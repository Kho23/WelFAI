# 🏥 WelfareMatch-AI
> **장애인 인적사항 기반 맞춤형 복지 서비스 자동 매칭 시스템**

본 프로젝트는 복잡한 복지 정책 속에서 장애인 개개인이 누릴 수 있는 혜택을 놓치지 않도록, 머신러닝(ML)과 거대언어모델(LLM)을 활용하여 최적의 서비스를 추천하고 상담을 제공하는 솔루션입니다.

---

## 📌 Project Overview
- **목적**: 복지 사각지대 해소 및 행정 효율화
- **핵심 기능**: 
  - 인적사항(나이, 소득, 장애유형 등) 기반 수혜 자격 자동 판별
  - 유사 사례 기반(KNN) 맞춤형 서비스 추천
  - LLM을 활용한 친절한 복지 가이드 및 대화형 상담

---

## 🛠️ Tech Stack & Learning Path
머신러닝 기초부터 운영(MLOps)까지 단계별로 학습하며 적용하고 있습니다.

### 1. Machine Learning (Core Logic)
- **Library**: `Scikit-learn`, `Pandas`, `NumPy`
- **Algorithms**: 
  - **지도 학습**: 선형 회귀(Linear Regression)를 통한 수혜 금액 예측, 분류(Classification)를 통한 자격 판별
  - **비지도 학습**: 군집화(Clustering)를 통한 유사 사용자 그룹핑 및 특성 추출
- **Study Log**: [Hand-on Machine Learning 3판] 기반 이론 및 실습 정리 중

### 2. Large Language Model (Interface)
- **Framework**: `LangChain` / `OpenAI API`
- **Role**: 복지 법령 데이터 기반의 RAG(검색 증강 생성) 상담 시스템 구축 예정

### 3. MLOps (Deployment)
- **Tools**: `Docker`, `GitHub Actions`
- **Goal**: 새로운 정책 업데이트 시 모델 재학습 및 배포 파이프라인 자동화

---

## 📊 Data Pipeline (Example)
머신러닝 모델 학습을 위해 사용되는 데이터 구조입니다.

| 데이터 구분 | 변수명 (Features) | 설명 |
| :--- | :--- | :--- |
| **Input (X)** | `Age`, `Income_Level`, `Disability_Type`, `Region` | 사용자 인적사항 및 소득 정보 |
| **Target (y)** | `Service_ID`, `Eligibility_Score` | 매칭된 서비스 코드 및 수혜 가능 점수 |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install scikit-learn pandas matplotlib
Installation
git clone [https://github.com/사용자이름/WelfareMatch-AI.git](https://github.com/사용자이름/WelfareMatch-AI.git)
cd WelfareMatch-AI
python practice.py
```
