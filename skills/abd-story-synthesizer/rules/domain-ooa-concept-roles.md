---
title: State Model — Wirfs-Brock Role Stereotypes
impact: MEDIUM
tags: discovery, domain
---

## Concept Roles (Optional)

When clarifying how a concept participates in interactions, you may assign a **role**:

| Role | Responsibility | Example |
|------|----------------|---------|
| **Information Holder** | Knows and provides information | Customer, Order, Product |
| **Structurer** | Maintains relationships between objects | Cart (holds line items) |
| **Service Provider** | Performs work; often stateless | TaxCalculator, Validator |
| **Coordinator** | Delegates to others | CheckoutController |
| **Controller** | Handles system events; represents use case | ProcessOrderHandler |
| **Interfacer** | Connects to outside world | PaymentGateway, EmailSender |
