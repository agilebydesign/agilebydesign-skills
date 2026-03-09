---
title: State Model — Standard Types for Properties
impact: HIGH
tags: discovery, domain
---

## Standard Types for Properties

**DO** use standard types for Properties when defining concepts:

| Type | Use when | Example |
|------|----------|---------|
| **String** | Text, names, labels | `Customer.name`, `Product.sku` |
| **Number** | Quantities, amounts, counts | `Cart.total`, `LineItem.quantity` |
| **Boolean** | Yes/no, flags | `Order.isPaid`, `Cart.isEmpty` |
| **List** | Ordered collection | `Cart.lineItems` (List of LineItem) |
| **Dictionary** | Key-value mapping | `Product.attributes`, `Config.settings` |
| **UniqueID** | Identifier, reference | `Order.customerId`, `LineItem.productId` |
| **Instant** | Point in time (ISO 8601) | `Order.createdAt`, `Payment.processedAt` |

Use `List<T>` or `Dictionary<K,V>` when element types matter.
