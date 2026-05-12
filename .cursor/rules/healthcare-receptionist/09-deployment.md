# Healthcare Receptionist - Production Deployment

## Overview

Complete guide for deploying Healthcare Receptionist domain to production with:
- Infrastructure setup
- Security configuration
- Monitoring & alerting
- Scaling strategies
- Disaster recovery

---

## Infrastructure Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       Load Balancer (ALB)                     │
│                  TLS 1.2+ (SSL Certificate)                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                  │
┌───────▼──────────┐            ┌─────────▼────────┐
│  Agent Instance  │            │  Agent Instance  │
│  (Auto-scaling)  │            │  (Auto-scaling)  │
│  GPT-4o via      │            │  GPT-4o via      │
│  LLM provider    │            │  LLM provider    │
└───────┬──────────┘            └─────────┬────────┘
        │                                  │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼─────────────────────┐
        │     FHIR Resource Store              │
        │     (PostgreSQL + JSONB)             │
        │     - Patient, Appointment, Coverage │
        │     - Observation, CarePlan, Task    │
        └────────────────┬─────────────────────┘
                         │
        ┌────────────────▼─────────────────────┐
        │     MCP Server Integration Layer     │
        │     - calendar, email, sms, tasks    │
        │     - pdf-generator, google-search   │
        └──────────────────────────────────────┘
```

---

## 1. Infrastructure Setup

### 1.1 AWS Architecture
```yaml
# infrastructure/terraform/main.tf
provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "healthcare_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "healthcare-receptionist-vpc"
    Environment = "production"
    HIPAA       = "compliant"
  }
}

# Private subnets (for agent instances)
resource "aws_subnet" "private_subnets" {
  count             = 2
  vpc_id            = aws_vpc.healthcare_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "healthcare-private-subnet-${count.index + 1}"
  }
}

# RDS PostgreSQL (for FHIR resources)
resource "aws_db_instance" "fhir_store" {
  identifier              = "healthcare-fhir-store"
  engine                  = "postgres"
  engine_version          = "15.4"
  instance_class          = "db.t3.medium"
  allocated_storage       = 100
  storage_encrypted       = true  # HIPAA requirement
  kms_key_id             = aws_kms_key.hipaa_key.arn
  
  username = "fhir_admin"
  password = var.db_password  # Store in AWS Secrets Manager
  
  backup_retention_period = 30  # HIPAA: 30-day retention
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  vpc_security_group_ids = [aws_security_group.fhir_db_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.fhir_subnet_group.name
  
  multi_az               = true  # High availability
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
  
  tags = {
    Name        = "healthcare-fhir-store"
    Environment = "production"
    HIPAA       = "compliant"
  }
}

# ECS Fargate (for agent instances)
resource "aws_ecs_cluster" "healthcare_cluster" {
  name = "healthcare-receptionist-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "healthcare_agent" {
  name            = "healthcare-receptionist-agent"
  cluster         = aws_ecs_cluster.healthcare_cluster.id
  task_definition = aws_ecs_task_definition.agent_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets         = aws_subnet.private_subnets[*].id
    security_groups = [aws_security_group.agent_sg.id]
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.agent_tg.arn
    container_name   = "healthcare-agent"
    container_port   = 8000
  }
}

# KMS for encryption (HIPAA requirement)
resource "aws_kms_key" "hipaa_key" {
  description             = "KMS key for HIPAA data encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

# S3 for audit logs (immutable)
resource "aws_s3_bucket" "hipaa_audit_logs" {
  bucket = "healthcare-hipaa-audit-logs-${var.account_id}"
  
  versioning {
    enabled = true
  }
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "aws:kms"
        kms_master_key_id = aws_kms_key.hipaa_key.arn
      }
    }
  }
  
  lifecycle_rule {
    enabled = true
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 2555  # 7 years (HIPAA requirement)
    }
  }
  
  object_lock_configuration {
    object_lock_enabled = "Enabled"
    
    rule {
      default_retention {
        mode = "COMPLIANCE"
        years = 7
      }
    }
  }
}
```

### 1.2 Database Schema
```sql
-- FHIR Resource Store (PostgreSQL)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Patients table
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mrn VARCHAR(50) UNIQUE NOT NULL,
    fhir_resource JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL  -- Soft delete for audit
);

CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_fhir ON patients USING GIN(fhir_resource);

-- Appointments table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id),
    fhir_resource JSONB NOT NULL,
    status VARCHAR(20) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_start ON appointments(start_time);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Coverage (Insurance) table
CREATE TABLE coverage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id),
    fhir_resource JSONB NOT NULL,
    payor VARCHAR(255) NOT NULL,
    member_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_coverage_patient ON coverage(patient_id);
CREATE INDEX idx_coverage_member_id ON coverage(member_id);

-- Audit log (immutable)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP DEFAULT NOW(),
    user_id VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    patient_id UUID,
    ip_address INET,
    details JSONB,
    CONSTRAINT no_update CHECK (false)  -- Prevent updates
);

-- Function to prevent deletions
CREATE OR REPLACE FUNCTION prevent_audit_deletion()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit log entries cannot be deleted (HIPAA requirement)';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_log_no_delete
BEFORE DELETE ON audit_log
FOR EACH ROW EXECUTE FUNCTION prevent_audit_deletion();

-- Row-level security (for multi-tenancy)
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE coverage ENABLE ROW LEVEL SECURITY;
```

---

## 2. Security Configuration

### 2.1 TLS/SSL Configuration
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name api.healthcareclinic.com;
    
    # SSL certificates
    ssl_certificate /etc/nginx/ssl/clinic.crt;
    ssl_certificate_key /etc/nginx/ssl/clinic.key;
    
    # TLS 1.2+ only (HIPAA requirement)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    
    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://agent_backend;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 2.2 IAM Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "FHIRStoreAccess",
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances",
        "rds:Connect"
      ],
      "Resource": "arn:aws:rds:us-east-1:*:db:healthcare-fhir-store"
    },
    {
      "Sid": "AuditLogWrite",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::healthcare-hipaa-audit-logs-*/*"
    },
    {
      "Sid": "KMSDecrypt",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:us-east-1:*:key/*",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "rds.us-east-1.amazonaws.com"
        }
      }
    }
  ]
}
```

### 2.3 Secrets Management
```python
# config/secrets.py
import boto3
from botocore.exceptions import ClientError

class SecretsManager:
    """Manage secrets via AWS Secrets Manager"""
    
    def __init__(self):
        self.client = boto3.client('secretsmanager', region_name='us-east-1')
    
    def get_secret(self, secret_name: str) -> dict:
        """Retrieve secret from AWS Secrets Manager"""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            raise Exception(f"Failed to retrieve secret: {e}")
    
    def get_db_credentials(self) -> dict:
        """Get FHIR database credentials"""
        return self.get_secret('healthcare/fhir-store/credentials')
    
    def get_api_keys(self) -> dict:
        """Get MCP server API keys"""
        return self.get_secret('healthcare/mcp-servers/api-keys')

# Usage
secrets = SecretsManager()
db_creds = secrets.get_db_credentials()
# {
#   "username": "fhir_admin",
#   "password": "...",
#   "host": "healthcare-fhir-store.abc123.us-east-1.rds.amazonaws.com",
#   "port": 5432,
#   "database": "fhir"
# }
```

---

## 3. Monitoring & Alerting

### 3.1 CloudWatch Metrics
```python
# monitoring/metrics.py
import boto3
from datetime import datetime

class HealthcareMetrics:
    """Custom CloudWatch metrics for healthcare domain"""
    
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'Healthcare/Receptionist'
    
    def record_patient_intake(self, success: bool, duration_ms: float):
        """Record patient intake metrics"""
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=[
                {
                    'MetricName': 'PatientIntakeCount',
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': datetime.now(),
                    'Dimensions': [
                        {'Name': 'Status', 'Value': 'Success' if success else 'Failed'}
                    ]
                },
                {
                    'MetricName': 'PatientIntakeDuration',
                    'Value': duration_ms,
                    'Unit': 'Milliseconds',
                    'Timestamp': datetime.now()
                }
            ]
        )
    
    def record_triage_assessment(self, category: str, safety_critical: bool):
        """Record clinical triage metrics"""
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=[
                {
                    'MetricName': 'TriageAssessment',
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': datetime.now(),
                    'Dimensions': [
                        {'Name': 'Category', 'Value': category},
                        {'Name': 'SafetyCritical', 'Value': str(safety_critical)}
                    ]
                }
            ]
        )
    
    def record_hipaa_violation(self, violation_type: str):
        """Record HIPAA violations (CRITICAL)"""
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=[
                {
                    'MetricName': 'HIPAAViolation',
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': datetime.now(),
                    'Dimensions': [
                        {'Name': 'ViolationType', 'Value': violation_type}
                    ]
                }
            ]
        )
```

### 3.2 CloudWatch Alarms
```yaml
# monitoring/alarms.yaml
alarms:
  # Safety-critical: Triage failures
  - name: TriageSafetyFailure
    metric: TriageAssessment
    dimensions:
      - SafetyCritical: "true"
    statistic: Sum
    period: 60
    evaluation_periods: 1
    threshold: 1
    comparison_operator: GreaterThanOrEqualToThreshold
    alarm_actions:
      - arn:aws:sns:us-east-1:123456789:healthcare-critical-alerts
    treat_missing_data: notBreaching
    description: "CRITICAL: Safety-critical triage failure detected"
  
  # HIPAA violations
  - name: HIPAAViolationDetected
    metric: HIPAAViolation
    statistic: Sum
    period: 300
    evaluation_periods: 1
    threshold: 1
    comparison_operator: GreaterThanOrEqualToThreshold
    alarm_actions:
      - arn:aws:sns:us-east-1:123456789:healthcare-compliance-alerts
    description: "HIPAA violation detected - immediate investigation required"
  
  # High error rate
  - name: HighPatientIntakeErrorRate
    metric: PatientIntakeCount
    dimensions:
      - Status: "Failed"
    statistic: Sum
    period: 300
    evaluation_periods: 2
    threshold: 10
    comparison_operator: GreaterThanThreshold
    alarm_actions:
      - arn:aws:sns:us-east-1:123456789:healthcare-ops-alerts
```

### 3.3 Logging
```python
# logging/structured_logger.py
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logging with PHI masking"""
    
    def __init__(self):
        self.logger = logging.getLogger('healthcare')
        self.phi_detector = PHIDetector()
    
    def log(self, level: str, event: str, context: dict = None):
        """Log with automatic PHI masking"""
        # Mask PHI in context
        safe_context = self._mask_phi(context or {})
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'event': event,
            'context': safe_context
        }
        
        self.logger.log(
            getattr(logging, level.upper()),
            json.dumps(log_entry)
        )
    
    def _mask_phi(self, context: dict) -> dict:
        """Mask PHI in context"""
        safe_context = {}
        for key, value in context.items():
            if key in ['patient_name', 'mrn', 'ssn']:
                safe_context[key] = f"****{str(value)[-4:]}"
            elif key in ['diagnosis', 'medication']:
                safe_context[key] = '[REDACTED]'
            else:
                safe_context[key] = value
        return safe_context
```

---

## 4. Scaling Strategy

### 4.1 Auto-scaling Configuration
```yaml
# auto-scaling/config.yaml
auto_scaling:
  target_tracking:
    - metric: CPUUtilization
      target_value: 70
      scale_in_cooldown: 300
      scale_out_cooldown: 60
    
    - metric: RequestCountPerTarget
      target_value: 1000
      scale_in_cooldown: 300
      scale_out_cooldown: 60
  
  min_capacity: 2
  max_capacity: 10
  
  scheduled_scaling:
    - name: BusinessHoursScaleUp
      schedule: "cron(0 7 * * MON-FRI)"
      min_capacity: 4
      max_capacity: 10
    
    - name: BusinessHoursScaleDown
      schedule: "cron(0 19 * * MON-FRI)"
      min_capacity: 2
      max_capacity: 6
```

### 4.2 Database Connection Pooling
```python
# database/pool.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

class FHIRDatabasePool:
    """Connection pool for FHIR database"""
    
    def __init__(self, db_url: str):
        self.engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=20,          # Base connections
            max_overflow=10,       # Additional connections under load
            pool_timeout=30,       # Connection timeout
            pool_recycle=3600,     # Recycle connections every hour
            pool_pre_ping=True     # Verify connections before use
        )
    
    def get_connection(self):
        return self.engine.connect()
```

---

## 5. Disaster Recovery

### 5.1 Backup Strategy
```yaml
# backup/strategy.yaml
backup:
  rds:
    automated_backups:
      retention_period: 30  # 30 days
      backup_window: "03:00-04:00"  # UTC
      preferred_backup_window: "sun:03:00-sun:04:00"
    
    manual_snapshots:
      frequency: weekly
      retention: 90  # 90 days
    
    point_in_time_recovery:
      enabled: true
      recovery_window: 30  # days
  
  s3_audit_logs:
    versioning: enabled
    replication:
      destination_bucket: healthcare-audit-logs-dr-us-west-2
      destination_region: us-west-2
    
    lifecycle:
      - days: 90
        storage_class: GLACIER
      - days: 2555  # 7 years (HIPAA)
        action: expire
```

### 5.2 Recovery Procedures
```bash
# disaster-recovery/restore.sh

#!/bin/bash
# Disaster Recovery - RDS Restore

# 1. Identify latest snapshot
SNAPSHOT_ID=$(aws rds describe-db-snapshots \
  --db-instance-identifier healthcare-fhir-store \
  --query 'DBSnapshots[0].DBSnapshotIdentifier' \
  --output text)

# 2. Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier healthcare-fhir-store-restored \
  --db-snapshot-identifier $SNAPSHOT_ID \
  --db-instance-class db.t3.medium \
  --multi-az \
  --publicly-accessible false

# 3. Wait for restore to complete
aws rds wait db-instance-available \
  --db-instance-identifier healthcare-fhir-store-restored

# 4. Update application configuration
kubectl set env deployment/healthcare-agent \
  DB_HOST=healthcare-fhir-store-restored.abc123.us-east-1.rds.amazonaws.com

echo "Disaster recovery complete. RTO: 15 minutes, RPO: 5 minutes"
```

---

## 6. Production Checklist

### Pre-Deployment
- [ ] All secrets stored in AWS Secrets Manager
- [ ] TLS 1.2+ configured
- [ ] Database encrypted at rest (KMS)
- [ ] Audit logging to immutable S3 bucket
- [ ] Row-level security enabled on patient data
- [ ] CloudWatch alarms configured
- [ ] Auto-scaling policies set
- [ ] Backup and disaster recovery tested
- [ ] HIPAA compliance audit completed

### Post-Deployment
- [ ] Verify TLS certificate valid
- [ ] Test database connectivity
- [ ] Verify audit logs writing to S3
- [ ] Test CloudWatch alarms (simulate failures)
- [ ] Verify auto-scaling triggers
- [ ] Run load test (1000 requests/minute)
- [ ] Test disaster recovery restore procedure
- [ ] Document runbook for on-call engineers

---

## 7. Monitoring Dashboard

**CloudWatch Dashboard:** `Healthcare-Receptionist-Production`

**Widgets:**
1. **Patient Intake Success Rate** (%)
2. **Average Response Time** (ms)
3. **HIPAA Violations** (count) - CRITICAL
4. **Triage Safety Failures** (count) - CRITICAL
5. **API Error Rate** (%)
6. **Database Connection Pool** (utilization)
7. **Auto-scaling Events** (count)
8. **MCP Server Latency** (ms)

---

## Next Steps
- Review `06-hipaa-compliance.md` for security requirements
- Review `08-api-contracts.md` for API specifications
- Test disaster recovery procedures quarterly
- Conduct HIPAA compliance audit annually

**Production deployment complete!** 🎉

