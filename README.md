# COMP4442 — Service and Cloud Computing
## PolyU Exam Preparation Package

Open-book final exam prep materials (3 hours, 100 marks).

---

## Contents

| File | Description |
|------|-------------|
| `pastpapers_qa.docx` | Full model answers for all 3 past papers (2023, 2024, 2025) |
| `coding_questions.docx` | 7 programming questions: Flask CRUD, PySpark RDD/DataFrame, AWS Lambda, bug-spotting, from-scratch jobs |
| `exam_notes.docx` | 11-section open-book cheat sheet (print and bring to exam) |
| `build_pastpapers_qa.py` | Source script that generates `pastpapers_qa.docx` |
| `build_coding_questions.py` | Source script that generates `coding_questions.docx` |
| `build_exam_notes.py` | Source script that generates `exam_notes.docx` |

---

## Exam Notes — 11 Sections

1. Cloud Computing Fundamentals (NIST 5, IaaS/PaaS/SaaS, deployment models, cloud app types)
2. Virtualization (Type-1 vs Type-2, Xen + VM data path, cgroups/namespaces, Docker)
3. Kubernetes (control plane, workflow, objects, scheduling, kubectl)
4. Data Center Networking (Fat-Tree k³/4, DCell, SDN/OpenFlow, VXLAN)
5. Hadoop (Big Data 4Vs, HDFS, MapReduce phases, YARN, MR limitations, Hadoop ecosystem)
6. Apache Spark (architecture, RDD/DataFrame API, Spark MLlib, EMR stack)
7. SOA & Microservices (8 principles, ESB, service composition, stateful vs stateless, SQS/SNS)
8. AWS Services (Lambda, DynamoDB, S3, EC2, ECS/EKS, API Gateway, Cognito, IoT Core)
9. Flask & Cloud App Patterns (routes, boto3, MySQL, Elastic Beanstalk)
10. Past Paper Analysis (topic frequency, 2026 predictions, answer templates)
11. Coding Quick Reference (DataFrame/RDD skeletons, HTTP status codes, key numbers, pitfalls)

---

## Regenerate DOCX files

```bash
pip install python-docx
python build_pastpapers_qa.py
python build_coding_questions.py
python build_exam_notes.py
```

---

## Topics Covered

`Cloud` `AWS` `Flask` `PySpark` `Hadoop` `Spark` `Kubernetes` `Docker` `Virtualization` `Xen` `MapReduce` `YARN` `HDFS` `DynamoDB` `Lambda` `SQS` `SNS` `Kinesis` `SOA` `REST` `Fat-Tree` `SDN`
