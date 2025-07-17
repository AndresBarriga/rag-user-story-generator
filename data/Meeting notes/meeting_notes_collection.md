# TYNGO Meeting Notes Collection

## Weekly Development Team Meeting - Jul 15, 2025

**Date:** July 15, 2025  
**Time:** 9:00 AM - 10:30 AM PST  
**Attendees:** Sarah Chen (Tech Lead), Mike Rodriguez (Backend Dev), Lisa Wang (Frontend Dev), James Thompson (QA Lead), David Kim (Product Manager)

### Agenda Items

#### 1. Sprint 23 Progress Review
- **Table-Side Ordering Feature:** 85% complete
  - Mobile UI components finalized
  - Oracle Simphony integration testing in progress
  - Stripe payment flow needs final validation
- **Analytics Dashboard:** Blocked waiting for Oracle data schema
- **Performance Optimization:** React components lazy loading implemented

#### 2. Stripe Integration Status
- Live pricing table integration: **COMPLETED**
- Subscription management portal: **IN TESTING**
- Webhook handling for payment events: **PENDING**
- Security review scheduled for Jul 18

#### 3. Blockers & Issues
- Oracle Simphony API rate limiting causing timeout issues
- Office 365 booking integration needs admin approval
- Responsive design issues on tablet devices (768px-1024px)

#### 4. Next Sprint Planning
- Focus on Oracle integration optimization
- Complete Stripe webhook implementation
- Begin work on real-time order updates feature

**Action Items:**
- Mike: Optimize Oracle API calls by Jul 18
- Lisa: Fix tablet responsive issues by Jul 17
- James: Complete Stripe payment testing by Jul 19
- David: Schedule client demo for Jul 25

---

## Refinement Call - Table-Side Ordering Feature - Sprint 23 - Jul 10, 2025

**Date:** July 10, 2025  
**Time:** 2:00 PM - 3:30 PM PST  
**Attendees:** Product Team + Development Team

### Feature Overview
**Epic:** Table-Side Ordering System  
**Story Points:** 13  
**Priority:** High

### Acceptance Criteria Refinement

#### User Story: "As a restaurant customer, I want to place orders directly from my table using a mobile device"

**Refined Acceptance Criteria:**
1. Customer scans QR code at table to access ordering interface
2. Mobile-first responsive design (320px-768px priority)
3. Integration with Oracle Simphony POS system
4. Real-time order status updates
5. Stripe payment processing with 3D Secure support
6. Order confirmation via SMS/email

#### Technical Requirements Discussed
- **Frontend:** React + TypeScript with Tailwind CSS
- **Backend:** Node.js API with Oracle Simphony integration
- **Payment:** Stripe Elements for secure card processing
- **Styling:** TYNGO brand colors (Blue: hsl(217, 91%, 60%))

#### Definition of Done
- [ ] Mobile UI passes accessibility tests (WCAG 2.1)
- [ ] Oracle Simphony integration tested with live POS
- [ ] Stripe payment flow tested with test cards
- [ ] Error handling for network failures
- [ ] Performance: < 3s load time on 3G
- [ ] Cross-browser testing (Chrome, Safari, Firefox)

**Concerns Raised:**
- Network reliability in restaurant environments
- Oracle API rate limiting (500 calls/hour)
- Stripe webhook reliability for order confirmation

**Sprint Commitment:** Feature will be demo-ready by Jul 22, 2025

---

## Backend Architecture Review - Stripe Integration - Jul 18, 2025

**Date:** July 18, 2025  
**Time:** 10:00 AM - 12:00 PM PST  
**Attendees:** Mike Rodriguez (Backend Lead), Sarah Chen (Tech Lead), Alex Johnson (DevOps), Emma Davis (Security Engineer)

### Architecture Overview

#### Current Stripe Integration Architecture
```
Frontend (React) → API Gateway → Node.js Backend → Stripe API
                                       ↓
                              Oracle Simphony POS
```

#### Key Components Reviewed

**1. Payment Processing Flow**
- Stripe Elements for secure card collection
- Payment Intent creation with metadata
- Webhook handling for payment confirmation
- Oracle Simphony order creation upon successful payment

**2. Subscription Management**
- Live pricing table: `prctbl_1RdSbDG13KD7SzkS3yYckCFn`
- Customer portal: `https://billing.stripe.com/p/login/test_3cIbJ11DO980ccdb2587K00`
- Automated billing cycle management

**3. Security Considerations**
- PCI DSS compliance through Stripe
- Webhook signature verification
- API key rotation strategy
- Rate limiting implementation

#### Technical Decisions Made

**Database Schema:**
- Orders table with Stripe payment_intent_id
- Customers table with Stripe customer_id
- Audit log for all payment events

**Error Handling:**
- Retry mechanism for failed Oracle API calls
- Fallback payment methods
- Graceful degradation for offline scenarios

**Performance Optimizations:**
- Connection pooling for Oracle connections
- Stripe webhook queue processing
- CDN for static assets

#### Security Review Results
- **PASSED:** Webhook signature validation
- **PASSED:** API key management
- **ACTION REQUIRED:** Implement payment data encryption at rest
- **ACTION REQUIRED:** Add rate limiting per customer

**Next Steps:**
- Implement encryption for sensitive data by Jul 25
- Deploy to staging environment by Jul 22
- Performance testing with load simulation

---

## Client Meeting - Sales Workflow Process - Jul 20, 2025

**Date:** July 20, 2025  
**Time:** 1:00 PM - 2:30 PM PST  
**Attendees:** David Kim (Product Manager), Jennifer Walsh (Sales Director), Restaurant Owner - Tony Marcelli, Operations Manager - Maria Santos

### Meeting Objectives
Review current sales workflow and identify optimization opportunities for TYNGO Staff Order system implementation.

### Current Restaurant Workflow Analysis

#### Traditional Order Process (Before TYNGO)
1. Customer seated → Server takes order → Kitchen preparation → Payment processing
2. **Pain Points Identified:**
   - Order accuracy issues (15% error rate)
   - Server bottlenecks during peak hours
   - Payment processing delays
   - Limited upselling opportunities

#### Proposed TYNGO Workflow
1. Customer scans QR code → Places order via mobile → Kitchen receives order → Automated payment
2. **Expected Improvements:**
   - 90% reduction in order errors
   - 25% faster table turnover
   - 18% increase in average order value
   - Real-time inventory updates

### Sales Process Requirements

#### Customer Onboarding Flow
1. **Demo Scheduling:** Office 365 integration for calendar booking
2. **Pricing Presentation:** Stripe pricing table with live calculations
3. **Contract Signing:** Digital signature integration
4. **Implementation:** 2-week onboarding process

#### Staff Training Requirements
- 4-hour initial training session
- Mobile app usage demonstration
- Oracle Simphony integration walkthrough
- Troubleshooting common issues

### Key Decisions Made

**Pricing Strategy:**
- Tiered subscription model via Stripe
- Per-table pricing structure
- 30-day free trial period
- Custom enterprise pricing for 50+ tables

**Implementation Timeline:**
- Week 1: System setup and Oracle integration
- Week 2: Staff training and soft launch
- Week 3: Full deployment and optimization
- Week 4: Performance review and adjustments

**Success Metrics:**
- Order accuracy: Target 95%+
- Table turnover: Target 20% improvement
- Customer satisfaction: Target 4.5/5 stars
- Revenue increase: Target 15% within 60 days

#### Next Steps
- Schedule technical integration meeting for Jul 25
- Prepare demo environment for client testing
- Create customized pricing proposal
- Develop implementation project plan

**Action Items:**
- David: Prepare demo environment by Jul 23
- Jennifer: Create pricing proposal by Jul 22
- Tony: Identify 5 tables for pilot testing
- Maria: Schedule staff training sessions