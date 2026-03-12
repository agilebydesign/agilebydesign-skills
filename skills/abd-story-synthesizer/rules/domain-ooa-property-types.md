---
title: State Model — Standard Types for Properties
impact: HIGH
tags: discovery, domain
scanner: domain_property_types
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

| **EnumType** | Fixed set of valid values | `ModifierType type {bonus, penalty}`, `ActionType action_type {standard, move, free, reaction}` |

Use `List<T>` or `Dictionary<K,V>` when element types matter.

**DO** use a named enum type when a property has a constrained set of valid values. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** use `String` with parenthetical options (e.g., `String type (bonus/penalty)`). Strings imply free-form text; constrained options are a distinct type.

- Example (wrong): `String type (bonus/penalty)`, `String attack_type (close/ranged)`.
- Example (right): `ModifierType type {bonus, penalty}`, `AttackType attack_type {close, ranged}`.
