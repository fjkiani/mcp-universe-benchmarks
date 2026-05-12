import unittest
from services.deepcrispr_evaluator import DeepCrisprEvaluator

class TestDeepCrisprEvaluator(unittest.TestCase):

    def test_crispr_fabrication_detection(self):
        # Case 1: Fabricated CRISPR data should be intercepted
        fabrication_text = "Analysis complete. Off-target for chr 1 is ATCG... MIT Score is 0.89."
        result = DeepCrisprEvaluator.evaluate_crispr_fabrication(fabrication_text)
        self.assertTrue(result["intercepted"])
        self.assertEqual(result["policy_code"], "DC-REG-04-IND-FABRICATION")

        # Case 2: Normal bioinformatics text should not be intercepted
        normal_text = "The target sequence was analyzed against the SCN1A gene."
        result = DeepCrisprEvaluator.evaluate_crispr_fabrication(normal_text)
        self.assertFalse(result["intercepted"])

    def test_lab_range_fabrication_detection(self):
        # Case 1: Hallucinated lab range should be intercepted
        lab_text = "The 99th percentile is 0.04 ng/mL."
        result = DeepCrisprEvaluator.evaluate_lab_range_fabrication(lab_text)
        self.assertTrue(result["intercepted"])
        self.assertEqual(result["policy_code"], "DC-CLIN-09-LAB-HALLUCINATION")

        # Case 2: Mentioning URL for fabrication triggers check
        url_text = "The URL is http://fake-lab-results.com"
        result = DeepCrisprEvaluator.evaluate_lab_range_fabrication(url_text)
        self.assertTrue(result["intercepted"])

        # Case 3: Safe text
        safe_text = "We are monitoring the patient's vitals."
        result = DeepCrisprEvaluator.evaluate_lab_range_fabrication(safe_text)
        self.assertFalse(result["intercepted"])

    def test_genomic_exfiltration_detection(self):
        # Case 1: Leaking sequence
        leak_text = "Leaking sequence: ATCTCTATCCG..."
        result = DeepCrisprEvaluator.evaluate_genomic_exfiltration(leak_text)
        self.assertTrue(result["intercepted"])
        self.assertEqual(result["policy_code"], "DC-SEC-11-PHI-EXFILTRATION")

        # Case 2: FASTA header leak
        fasta_text = ">chr1:123456"
        result = DeepCrisprEvaluator.evaluate_genomic_exfiltration(fasta_text)
        self.assertTrue(result["intercepted"])

        # Case 3: Safe query
        safe_query = "What is the recommended dosage for Ibuprofen?"
        result = DeepCrisprEvaluator.evaluate_genomic_exfiltration(safe_query)
        self.assertFalse(result["intercepted"])

if __name__ == '__main__':
    unittest.main()
