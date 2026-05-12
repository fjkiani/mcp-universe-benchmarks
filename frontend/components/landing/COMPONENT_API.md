# Landing Page Component API

## Standard Component Pattern

All landing page components follow this pattern:

```jsx
export function ComponentName({ config }) {
  // Support both new config structure and old props (backward compat)
  const content = config?.content || { /* fallback to old props */ }
  const visual = config?.visual || {}
  const behavior = config?.behavior || {}
  
  return (
    <section className={visual.background?.gradient || 'bg-white'}>
      {/* Component renders based on config */}
    </section>
  )
}
```

---

## Component APIs

### **Hero Component**

```jsx
<Hero config={heroConfig} />
// OR (backward compat)
<Hero 
  headline="..."
  subheadline="..."
  primaryCTA={...}
  secondaryCTAs={...}
/>
```

**Config Structure:**
```javascript
{
  content: {
    headline: string,
    subheadline: string,
    primaryCTA: { text: string, link: string, note?: string },
    secondaryCTAs: [{ text: string, link: string }],
    badge: { icon: string, text: string },
    stats: [{ icon: string, value: string, label: string }]
  },
  visual: {
    background: { type: string, colors: string[], gradient: string },
    headline: { gradient: string, size: string },
    badge: { gradient: string, border: string, animation: string },
    stats: [{ gradient: string, animation: string, delay: string }]
  },
  behavior: {
    ctaHover: string,
    statsHover: string,
    animation: { stagger: boolean, duration: number }
  }
}
```

---

### **ProblemStatement Component**

```jsx
<ProblemStatement config={problemConfig} />
// OR (backward compat)
<ProblemStatement
  headline="..."
  description="..."
  problems={[...]}
  result="..."
/>
```

**Config Structure:**
```javascript
{
  content: {
    headline: string,
    description: string,
    problems: [{ icon: string, text: string }],
    result: string
  },
  visual: {
    background: { gradient: string },
    icon: { color: string, size: string },
    cards: { gradient: string, border: string }
  },
  behavior: {
    cardHover: string,
    animation: { stagger: boolean }
  }
}
```

---

### **Solution Component**

```jsx
<Solution config={solutionConfig} />
// OR (backward compat)
<Solution
  headline="..."
  description="..."
  whatItDoes={[...]}
  whatItReplaces={[...]}
/>
```

**Config Structure:**
```javascript
{
  content: {
    headline: string,
    description: string,
    whatItDoes: string[],
    whatItReplaces: string[]
  },
  visual: {
    background: { gradient: string },
    whatItDoesCard: { gradient: string, border: string },
    whatItReplacesCard: { gradient: string, border: string }
  },
  behavior: {
    cardHover: string,
    animation: { stagger: boolean }
  }
}
```

---

### **HowItWorks Component**

```jsx
<HowItWorks config={howItWorksConfig} />
// OR (backward compat)
<HowItWorks
  headline="..."
  subheadline="..."
  steps={[...]}
/>
```

**Config Structure:**
```javascript
{
  content: {
    headline: string,
    subheadline: string,
    steps: [{ 
      number: number, 
      title: string, 
      description: string, 
      icon: string 
    }]
  },
  visual: {
    background: { gradient: string },
    stepCards: { gradient: string, border: string },
    connector: { color: string, style: string }
  },
  behavior: {
    stepHover: string,
    animation: { stagger: boolean, direction: string }
  }
}
```

---

### **Pricing Component**

```jsx
<Pricing config={pricingConfig} />
// OR (backward compat)
<Pricing
  headline="..."
  tiers={[...]}
  includedInAll={[...]}
/>
```

**Config Structure:**
```javascript
{
  content: {
    headline: string,
    tiers: [{
      name: string,
      price: string,
      period: string,
      features: string[],
      cta: { text: string, link: string },
      popular?: boolean
    }],
    includedInAll: string[]
  },
  visual: {
    background: { gradient: string },
    popularBadge: { gradient: string, color: string },
    tierCards: { gradient: string, border: string }
  },
  behavior: {
    tierHover: string,
    animation: { stagger: boolean }
  }
}
```

---

### **FAQ Component**

```jsx
<FAQ config={faqConfig} />
// OR (backward compat)
<FAQ faqs={[...]} />
```

**Config Structure:**
```javascript
{
  content: {
    headline?: string,
    faqs: [{
      question: string,
      answer: string
    }]
  },
  visual: {
    background: { gradient: string },
    accordion: { border: string, hover: string }
  },
  behavior: {
    animation: { duration: number, easing: string }
  }
}
```

---

## Visual Constants Usage

All components can use visual constants from the domain's `visual-constants.js`:

```javascript
import { VISUAL_THEME } from '../../domains/{domain}/constants'

// Use in component
<section className={VISUAL_THEME.gradients.hero}>
  <h1 className={VISUAL_THEME.typography.hero.headline}>
    {content.headline}
  </h1>
</section>
```

---

## Best Practices

1. **Always support both config and props** - Backward compatibility
2. **Use visual constants** - Don't hardcode styles
3. **Separate content/visual/behavior** - Makes it easy to customize
4. **Provide sensible defaults** - Components should work without config
5. **Document config structure** - Makes it easy for others to use

---

**Status:** ✅ **Component API Documented**

All components follow this pattern, making them reusable and easy to customize for different products. [[memory:10794303]]






