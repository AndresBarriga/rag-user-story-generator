# TYNGO Functional Documentation Collection

## Functional Specification - Authentication Module v2.1

**Document Version:** 2.1  
**Last Updated:** July 8, 2025  
**Author:** Sarah Chen (Tech Lead)  
**Reviewers:** Mike Rodriguez (Backend), Emma Davis (Security)

### Overview
This document specifies the authentication module for TYNGO Staff Order system, including customer authentication, staff authentication, and integration with Oracle Simphony POS system.

### Authentication Requirements

#### 1. Customer Authentication
**Purpose:** Secure customer access to table-side ordering system

**Authentication Methods:**
- **Primary:** QR Code + Table Number verification
- **Secondary:** SMS OTP for payment confirmation
- **Fallback:** Staff-assisted authentication

**User Flow:**
1. Customer scans QR code at table
2. System validates table number and availability
3. Session created with 2-hour timeout
4. Order placement requires SMS verification for payments > $50

#### 2. Staff Authentication
**Purpose:** Secure access to staff management interface

**Authentication Methods:**
- **Primary:** Username/Password with 2FA
- **Secondary:** SSO integration with restaurant's existing system
- **Admin:** Master key access for system configuration

**Role-Based Access Control:**
- **Server:** View orders, update order status, process payments
- **Kitchen:** View orders, update preparation status
- **Manager:** Full access, reporting, configuration
- **Admin:** System configuration, user management

#### 3. Oracle Simphony Integration Authentication
**Purpose:** Secure communication with POS system

**Authentication Flow:**
- API key authentication with Oracle Simphony
- Token refresh every 24 hours
- Encrypted connection (TLS 1.3)
- Rate limiting: 500 requests/hour per restaurant

### Security Requirements

#### Data Protection
- **Encryption:** AES-256 for data at rest
- **Transmission:** TLS 1.3 for all communications
- **Storage:** No credit card data stored locally
- **Compliance:** PCI DSS Level 1 through Stripe integration

#### Session Management
- **Customer Sessions:** 2-hour timeout, renewable
- **Staff Sessions:** 8-hour timeout, requires re-authentication
- **Token Storage:** Secure HTTP-only cookies
- **Logout:** Automatic session cleanup

#### Security Monitoring
- Failed authentication attempt tracking
- Suspicious activity alerts
- Audit logging for all authentication events
- Integration with security monitoring dashboard

### Technical Implementation

#### Database Schema
```sql
-- Users table for staff authentication
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('server', 'kitchen', 'manager', 'admin'),
    restaurant_id UUID,
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Customer sessions for table-side ordering
CREATE TABLE customer_sessions (
    id UUID PRIMARY KEY,
    table_number INTEGER NOT NULL,
    restaurant_id UUID,
    session_token VARCHAR(255) UNIQUE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP
);

-- Oracle integration tokens
CREATE TABLE oracle_tokens (
    id UUID PRIMARY KEY,
    restaurant_id UUID,
    access_token VARCHAR(500),
    refresh_token VARCHAR(500),
    expires_at TIMESTAMP,
    created_at TIMESTAMP
);
```

#### API Endpoints
- `POST /auth/customer/verify` - Customer QR code verification
- `POST /auth/staff/login` - Staff authentication
- `POST /auth/staff/logout` - Staff session termination
- `POST /auth/oracle/refresh` - Oracle token refresh
- `GET /auth/verify` - Session validation

### Integration Requirements

#### Stripe Integration
- Customer payment authentication via Stripe Elements
- 3D Secure authentication for international cards
- Webhook authentication for payment confirmations

#### Office 365 Integration
- SSO authentication for demo scheduling
- Calendar access for appointment booking
- Secure token exchange

### Testing Requirements

#### Unit Tests
- Authentication flow validation
- Token generation and verification
- Password hashing and validation
- Session management functions

#### Integration Tests
- Oracle Simphony API authentication
- Stripe payment authentication
- End-to-end customer authentication flow

#### Security Tests
- Penetration testing for authentication vulnerabilities
- SQL injection prevention
- Cross-site scripting (XSS) protection
- CSRF token validation

---

## Push Notifications System Requirements

**Document Version:** 1.0  
**Last Updated:** July 8, 2025  
**Author:** Lisa Wang (Frontend Lead)  
**Reviewers:** Mike Rodriguez (Backend), James Thompson (QA)

### System Overview
Real-time push notification system for TYNGO Staff Order platform to provide instant updates on order status, payment confirmations, and system alerts.

### Notification Types

#### 1. Customer Notifications
**Order Status Updates:**
- Order received confirmation
- Kitchen preparation started
- Order ready for pickup/delivery
- Payment processed successfully

**Marketing Notifications:**
- Daily specials and promotions
- Loyalty program updates
- Survey requests post-meal

#### 2. Staff Notifications
**Order Management:**
- New order received (Kitchen staff)
- Order modification requests
- Payment processing alerts
- Customer service requests

**System Notifications:**
- Oracle Simphony connection status
- Stripe payment failures
- System maintenance alerts

### Technical Requirements

#### Push Notification Channels
**Web Push (Primary):**
- Service worker implementation
- Browser notification API
- Progressive Web App support
- Offline notification queuing

**SMS (Secondary):**
- Twilio integration for critical alerts
- International SMS support
- Opt-in/opt-out management
- Rate limiting: 5 messages/day per customer

**Email (Fallback):**
- SMTP configuration for transactional emails
- HTML/text dual format
- Unsubscribe link compliance
- Delivery tracking and analytics

#### Real-time Communication
**WebSocket Implementation:**
- Real-time order status updates
- Kitchen display system integration
- Staff notification dashboard
- Connection recovery mechanisms

### Integration Points

#### Oracle Simphony Integration
- Order status webhooks
- Inventory level alerts
- POS system error notifications
- Real-time sales data updates

#### Stripe Integration
- Payment confirmation notifications
- Failed payment alerts
- Subscription status updates
- Refund processing notifications

### Notification Delivery Requirements

#### Performance Specifications
- **Delivery Time:** < 2 seconds for critical notifications
- **Reliability:** 99.9% delivery success rate
- **Scalability:** Support for 10,000+ concurrent connections
- **Battery Optimization:** Efficient mobile device resource usage

#### Personalization
- User preference management
- Notification scheduling (quiet hours)
- Language localization support
- Custom notification sounds

### Data Requirements

#### Notification Storage
```sql
-- Notification templates
CREATE TABLE notification_templates (
    id UUID PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    title_template VARCHAR(255),
    body_template TEXT,
    created_at TIMESTAMP
);

-- Notification delivery log
CREATE TABLE notification_log (
    id UUID PRIMARY KEY,
    user_id UUID,
    template_id UUID,
    channel VARCHAR(20),
    status VARCHAR(20),
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    error_message TEXT
);

-- User notification preferences
CREATE TABLE user_notification_preferences (
    user_id UUID PRIMARY KEY,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT FALSE,
    push_enabled BOOLEAN DEFAULT TRUE,
    quiet_hours_start TIME,
    quiet_hours_end TIME
);
```

#### Analytics and Tracking
- Notification delivery rates
- Open/click-through rates
- User engagement metrics
- System performance monitoring

---

## eCommerce Use Cases - Restaurant Inventory Management

**Document Version:** 1.0  
**Last Updated:** July 8, 2025  
**Author:** David Kim (Product Manager)  
**Reviewers:** Operations Team, Development Team

### Use Case Overview
This document outlines the eCommerce use cases for restaurant inventory management within the TYNGO Staff Order system, focusing on real-time inventory tracking and automated stock management.

### Primary Use Cases

#### Use Case 1: Real-Time Inventory Tracking
**Actor:** Kitchen Staff, Restaurant Manager  
**Goal:** Monitor ingredient and menu item availability in real-time

**Preconditions:**
- Oracle Simphony POS system is connected
- Inventory items are configured in the system
- Staff has appropriate access permissions

**Main Flow:**
1. Customer places order through table-side ordering system
2. System checks ingredient availability in real-time
3. If available, order is processed and inventory is decremented
4. If unavailable, customer is notified and alternative items suggested
5. Kitchen staff receives updated inventory levels on display
6. Manager receives low-stock alerts when thresholds are reached

**Alternative Flows:**
- **Insufficient Stock:** System suggests similar available items
- **System Offline:** Local inventory cache is used with sync on reconnection
- **Oracle Integration Error:** Manual inventory override by manager

#### Use Case 2: Automated Stock Replenishment
**Actor:** Restaurant Manager, Supplier System  
**Goal:** Automatically reorder ingredients when stock levels are low

**Preconditions:**
- Reorder points are configured for each ingredient
- Supplier integration is active
- Manager approval workflow is defined

**Main Flow:**
1. System monitors ingredient usage patterns
2. When stock level reaches reorder point, system generates purchase order
3. Manager receives approval notification
4. Upon approval, order is sent to supplier system
5. Delivery tracking integration updates expected arrival
6. Inventory is updated upon delivery confirmation

#### Use Case 3: Menu Item Availability Management
**Actor:** Kitchen Staff, Customers  
**Goal:** Dynamically update menu availability based on ingredient stock

**Preconditions:**
- Menu items are linked to required ingredients
- Recipe management is configured
- Real-time inventory tracking is active

**Main Flow:**
1. System continuously monitors ingredient levels
2. When required ingredients for menu item fall below threshold:
   - Item is automatically marked as unavailable
   - Customer-facing menu is updated in real-time
   - Kitchen staff receives notification
3. When ingredients are restocked:
   - Item availability is automatically restored
   - Menu updates reflect changes instantly

### Secondary Use Cases

#### Use Case 4: Waste Tracking and Analytics
**Actor:** Restaurant Manager, Kitchen Staff  
**Goal:** Track food waste and optimize ordering patterns

**Main Flow:**
1. Kitchen staff logs expired or wasted items
2. System tracks waste patterns by ingredient and time period
3. Analytics dashboard provides insights on waste reduction
4. Automated recommendations for order quantity adjustments
5. Integration with supplier systems for optimized ordering

#### Use Case 5: Seasonal Menu Management
**Actor:** Restaurant Manager, Chef  
**Goal:** Manage seasonal menu changes and ingredient availability

**Main Flow:**
1. Manager configures seasonal menu items and availability dates
2. System automatically updates inventory requirements
3. Supplier integration adjusts ordering patterns
4. Customer menu updates reflect seasonal changes
5. Analytics track seasonal performance metrics

### Technical Integration Requirements

#### Oracle Simphony Integration
```json
{
  "inventory_sync": {
    "endpoint": "/api/inventory/sync",
    "method": "POST",
    "frequency": "real-time",
    "data_format": "JSON",
    "authentication": "API_KEY"
  },
  "menu_updates": {
    "endpoint": "/api/menu/availability",
    "method": "PUT",
    "trigger": "inventory_change",
    "response_time": "< 2 seconds"
  }
}
```

#### Stripe Integration for Supplier Payments
- Automated supplier payment processing
- Purchase order financial tracking
- Cost analytics and reporting
- Budget management integration

### Data Requirements

#### Inventory Data Model
```sql
-- Inventory items
CREATE TABLE inventory_items (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    unit_of_measure VARCHAR(20),
    current_stock DECIMAL(10,2),
    reorder_point DECIMAL(10,2),
    max_stock DECIMAL(10,2),
    cost_per_unit DECIMAL(8,2),
    supplier_id UUID,
    last_updated TIMESTAMP
);

-- Menu item ingredients
CREATE TABLE menu_ingredients (
    menu_item_id UUID,
    ingredient_id UUID,
    quantity_required DECIMAL(8,2),
    is_critical BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (menu_item_id, ingredient_id)
);

-- Inventory transactions
CREATE TABLE inventory_transactions (
    id UUID PRIMARY KEY,
    item_id UUID,
    transaction_type VARCHAR(20), -- 'usage', 'restock', 'waste'
    quantity DECIMAL(10,2),
    reference_id UUID, -- order_id or purchase_order_id
    timestamp TIMESTAMP,
    notes TEXT
);
```

### Performance Requirements
- **Inventory Updates:** Real-time synchronization with Oracle Simphony
- **Menu Availability:** Updates within 2 seconds of inventory changes
- **Analytics Processing:** Daily batch processing for reporting
- **System Availability:** 99.9% uptime during restaurant hours

---

## Payment Process Flow - Stripe Integration

**Document Version:** 1.0  
**Last Updated:** July 8, 2025  
**Author:** Mike Rodriguez (Backend Lead)  
**Reviewers:** Sarah Chen (Tech Lead), Emma Davis (Security)

### Payment Process Overview
This document defines the complete payment processing flow for the TYNGO Staff Order system using Stripe integration, covering table-side ordering payments and subscription management.

### Payment Flow Architecture

#### System Components
```
Customer Mobile → React Frontend → Node.js API → Stripe API
                                       ↓
                                Oracle Simphony POS
                                       ↓
                                Kitchen Display System
```

### Primary Payment Flows

#### Flow 1: Table-Side Order Payment
**Actor:** Restaurant Customer  
**Goal:** Complete payment for table-side order

**Prerequisites:**
- Customer has placed order through mobile interface
- Order total is calculated and confirmed
- Stripe Elements is loaded and ready

**Main Payment Flow:**
1. **Order Confirmation:**
   - Customer reviews order summary
   - Tax and service charges are calculated
   - Total amount is displayed with breakdown

2. **Payment Method Selection:**
   - Credit/Debit card via Stripe Elements
   - Digital wallets (Apple Pay, Google Pay)
   - Saved payment methods for returning customers

3. **Payment Processing:**
   ```javascript
   // Payment Intent creation
   const paymentIntent = await stripe.paymentIntents.create({
     amount: orderTotal * 100, // Amount in cents
     currency: 'usd',
     automatic_payment_methods: {
       enabled: true,
     },
     metadata: {
       order_id: order.id,
       table_number: order.table_number,
       restaurant_id: order.restaurant_id
     }
   });
   ```

4. **3D Secure Authentication:**
   - Automatic 3D Secure authentication for international cards
   - SCA compliance for European customers
   - Biometric authentication for mobile wallets

5. **Payment Confirmation:**
   - Stripe webhook confirms payment success
   - Order status updated in Oracle Simphony
   - Customer receives confirmation notification
   - Kitchen receives order preparation notification

#### Flow 2: Subscription Payment Processing
**Actor:** Restaurant Manager  
**Goal:** Process monthly subscription payments

**Subscription Components:**
- **Live Pricing Table:** `prctbl_1RdSbDG13KD7SzkS3yYckCFn`
- **Customer Portal:** `https://billing.stripe.com/p/login/test_3cIbJ11DO980ccdb2587K00`
- **Automated Billing:** Monthly recurring payments

**Subscription Flow:**
1. **Plan Selection:**
   - Restaurant selects appropriate pricing tier
   - Table count and feature requirements determined
   - Trial period activation (30 days)

2. **Customer Creation:**
   ```javascript
   const customer = await stripe.customers.create({
     email: restaurant.email,
     name: restaurant.name,
     metadata: {
       restaurant_id: restaurant.id,
       table_count: restaurant.table_count
     }
   });
   ```

3. **Subscription Creation:**
   - Automatic recurring billing setup
   - Proration handling for plan changes
   - Invoice generation and delivery

### Error Handling and Recovery

#### Payment Failure Scenarios
**1. Insufficient Funds:**
- Immediate notification to customer
- Alternative payment method prompt
- Order held for 10 minutes before cancellation

**2. Network Connectivity Issues:**
- Automatic retry with exponential backoff
- Offline payment queue for network recovery
- Manual payment processing fallback

**3. Stripe API Failures:**
- Circuit breaker pattern implementation
- Fallback to manual payment processing
- Error logging and monitoring alerts

#### Recovery Mechanisms
```javascript
// Payment retry logic
const retryPayment = async (paymentIntent, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const result = await stripe.paymentIntents.confirm(paymentIntent.id);
      return result;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
};
```

### Security Implementation

#### PCI DSS Compliance
- **Scope Reduction:** Stripe handles all sensitive card data
- **SAQ-A Compliance:** Minimal PCI scope for merchant
- **Tokenization:** All card data tokenized by Stripe
- **Secure Transmission:** TLS 1.3 for all API communications

#### Webhook Security
```javascript
// Webhook signature verification
const verifyWebhookSignature = (payload, signature) => {
  try {
    const event = stripe.webhooks.constructEvent(
      payload,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET
    );
    return event;
  } catch (error) {
    throw new Error('Invalid webhook signature');
  }
};
```

#### Data Protection
- **Encryption:** Customer data encrypted at rest (AES-256)
- **Access Control:** Role-based access to payment data
- **Audit Logging:** All payment activities logged
- **Data Retention:** Automatic data purging after 7 years

### Integration Points

#### Oracle Simphony Integration
```javascript
// Order creation after successful payment
const createOracleOrder = async (paymentData) => {
  const orderData = {
    orderNumber: paymentData.metadata.order_id,
    tableNumber: paymentData.metadata.table_number,
    amount: paymentData.amount / 100,
    paymentMethod: 'STRIPE',
    timestamp: new Date().toISOString()
  };
  
  return await oracleAPI.createOrder(orderData);
};
```

#### Notification System Integration
- Payment confirmation notifications
- Failed payment alerts
- Subscription status updates
- Refund processing notifications

### Performance Requirements

#### Response Time Targets
- **Payment Intent Creation:** < 500ms
- **Payment Confirmation:** < 2 seconds
- **Webhook Processing:** < 1 second
- **Oracle Integration:** < 3 seconds

#### Scalability Specifications
- **Concurrent Payments:** 1,000+ simultaneous transactions
- **Peak Load:** 10,000 payments/hour
- **Availability:** 99.99% uptime
- **Failover:** < 30 seconds recovery time

### Monitoring and Analytics

#### Payment Metrics
- Success/failure rates by payment method
- Average transaction processing time
- Geographic payment distribution
- Subscription churn analysis

#### Alert Thresholds
- Payment failure rate > 5%
- Response time > 3 seconds
- Webhook processing delays > 10 seconds
- Oracle integration failures > 1%

### Testing Requirements

#### Test Payment Methods
```javascript
// Test card numbers for different scenarios
const testCards = {
  success: '4242424242424242',
  decline: '4000000000000002',
  requiresAuth: '4000002500003155',
  insufficientFunds: '4000000000009995'
};
```

#### Integration Testing
- End-to-end payment flow testing
- Webhook delivery testing
- Oracle Simphony integration testing
- Error scenario simulation
- Load testing with realistic traffic patterns