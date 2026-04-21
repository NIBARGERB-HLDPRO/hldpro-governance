# Deal Crm

> 49 nodes · cohesion 0.05

## Key Concepts

- **DealService** (9 connections) — `knocktracker/lib/services/dealService.ts`
- **ContactService** (7 connections) — `knocktracker/lib/services/contactService.ts`
- **CompanyService** (6 connections) — `knocktracker/lib/services/companyService.ts`
- **createEntity()** (6 connections) — `knocktracker/lib/api/helpers.ts`
- **handleSave()** (6 connections) — `knocktracker/app/crm/companies/new.tsx`
- **ActivityService** (5 connections) — `knocktracker/lib/services/activityService.ts`
- **updateEntity()** (5 connections) — `knocktracker/lib/api/helpers.ts`
- **.createCompany()** (4 connections) — `knocktracker/lib/services/companyService.ts`
- **.createContact()** (4 connections) — `knocktracker/lib/services/contactService.ts`
- **handleExport()** (3 connections) — `knocktracker/app/(main)/crm/contacts.tsx`
- **.createDeal()** (3 connections) — `knocktracker/lib/services/dealService.ts`
- **.moveDealToStage()** (3 connections) — `knocktracker/lib/services/dealService.ts`
- **.updateDeal()** (3 connections) — `knocktracker/lib/services/dealService.ts`
- **helpers.ts** (3 connections) — `knocktracker/lib/api/helpers.ts`
- **.createActivity()** (2 connections) — `knocktracker/lib/services/activityService.ts`
- **.updateActivity()** (2 connections) — `knocktracker/lib/services/activityService.ts`
- **.updateCompany()** (2 connections) — `knocktracker/lib/services/companyService.ts`
- **.getContacts()** (2 connections) — `knocktracker/lib/services/contactService.ts`
- **.updateContact()** (2 connections) — `knocktracker/lib/services/contactService.ts`
- **.exportContactsToCSV()** (2 connections) — `knocktracker/lib/crmService.ts`
- **.parseCSVContacts()** (2 connections) — `knocktracker/lib/crmService.ts`
- **handleMoveDeal()** (2 connections) — `knocktracker/app/(main)/crm/deals.tsx`
- **.getDealsByStage()** (2 connections) — `knocktracker/lib/services/dealService.ts`
- **.getPipelineStages()** (2 connections) — `knocktracker/lib/services/dealService.ts`
- **import.tsx** (2 connections) — `knocktracker/app/crm/contacts/import.tsx`
- *... and 24 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `knocktracker/app/(main)/crm/contacts.tsx`
- `knocktracker/app/(main)/crm/deals.tsx`
- `knocktracker/app/crm/companies/new.tsx`
- `knocktracker/app/crm/contacts/import.tsx`
- `knocktracker/app/crm/contacts/new.tsx`
- `knocktracker/app/crm/deals/new.tsx`
- `knocktracker/lib/api/helpers.ts`
- `knocktracker/lib/crmService.ts`
- `knocktracker/lib/services/activityService.ts`
- `knocktracker/lib/services/companyService.ts`
- `knocktracker/lib/services/contactService.ts`
- `knocktracker/lib/services/dealService.ts`

## Audit Trail

- EXTRACTED: 82 (71%)
- INFERRED: 34 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*