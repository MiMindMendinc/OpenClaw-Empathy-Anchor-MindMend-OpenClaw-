# Support resources

Informational routing only. This page records the contacts shipped in the scanner and Node skill, with the public page used to check them on **2026-08-17**. Availability is not guaranteed.

If someone may be in immediate danger, call or text **988** (United States) or contact local emergency services.

## Immediate (24/7, United States)

| Resource | How to reach | Source checked |
|----------|----------------|----------------|
| 988 Suicide & Crisis Lifeline | Call or text **988** | [988lifeline.org](https://988lifeline.org) |
| Crisis Text Line | Text **HOME** to **741741** | [crisistextline.org](https://www.crisistextline.org) |
| Michigan Crisis & Access Line (MiCAL) | Call or text **988**. MiCAL is Michigan’s statewide 988 call center. | [Michigan DHHS 988 / MiCAL](https://www.michigan.gov/mdhhs/keep-mi-healthy/mentalhealth/crisis-and-access-line) |
| Emergency services | **911** for immediate life-threatening emergencies | Public emergency number (US) |

MDHHS currently tells the public to use **988** for MiCAL/988 access in Michigan. This repository does **not** publish a separate MiCAL 1-844 number.

## Additional (not 24/7)

| Resource | How to reach | Hours | Source checked |
|----------|----------------|-------|----------------|
| NAMI HelpLine | 1-800-950-NAMI (6264) | Monday–Friday 10 a.m.–10 p.m. ET | [nami.org/support](https://www.nami.org/support) |
| NAMI Michigan | [namimi.org](https://namimi.org) | See organization site | [namimi.org](https://namimi.org) |
| Teen Line | Call **800-852-8336** or text **TEEN** to **839863** | Call 6–10 p.m. PT; text 6–9 p.m. PT. Outside those hours use 988. | [teenline.org](https://www.teenline.org) |

Do not describe NAMI HelpLine or Teen Line as 24/7 crisis services.

## Reproduce the in-product copy

Python source of truth: `backend/support_resources.py`

```bash
curl -s http://127.0.0.1:8000/api/v1/resources | python -m json.tool
```
