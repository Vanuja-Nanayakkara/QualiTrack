# Automated 7/0 Quality Inspection System

![License](https://img.shields.io/badge/license-MIT-blue) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Contributors](https://img.shields.io/badge/contributors-6-orange) ![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey) ![Tech Stack](https://img.shields.io/badge/tech-stack%20modern-blueviolet) ![Profile Views](https://komarev.com/ghpvc/?username=your-repo&color=blue)

![Header Image](assets/Logo.png)

The garment manufacturing industry faces challenges like inefficiencies, human errors, and delays in manual quality inspections. To address these, our project introduces an **Automated 7/0 Quality Inspection System** that leverages modern technologies such as **Machine Learning (ML)** and **Super-Resolution (SR)** to enhance accuracy, speed, and efficiency. The system aims to reduce defects, optimize workflows, and improve overall productivity for garment manufacturers.

---

## Features

### Key Features

- 🧠 **Automated Defect Detection**: Utilizes pre-trained YOLO (You Only Look Once) models to detect defects such as stitching errors, fabric tears, and stains.
- 🎨 **Image Enhancement**: Employs ESRGAN (Enhanced Super-Resolution Generative Adversarial Networks) to enhance low-quality images for more precise defect identification.
- ⏱️ **Real-Time Updates**: Provides instant notifications and updates through a supervisor dashboard for timely corrective actions.
- 📱 **Mobile Application**: A user-friendly app for garment inspectors to capture and process images directly on the production floor.
- 🌐 **Centralized Data Management**: Logs all inspection data in a cloud-based system for analytics, trend identification, and process optimization.

---

## Technologies Used

- **Frontend**: Flutter (Cross-platform mobile app development)
- **Backend**: Django (Data management and API integration)
- **Machine Learning Models**: YOLOv8 for object detection and ESRGAN for image enhancement
- **Database Management**: Cloud-based database for scalable and centralized storage
- **Collaboration Tools**: ClickUp, Slack, and Google Meet


---

## Benefits

- 🚀 **Increased Efficiency**: Automates inspections to minimize bottlenecks and delays.
- ✅ **Enhanced Accuracy**: Reduces human errors with consistent defect detection.
- 💰 **Cost Savings**: Lowers costs associated with rework, waste, and customer returns.
- 📊 **Improved Quality Control**: Real-time monitoring and comprehensive data analytics improve decision-making.

---

## Implementation Workflow


1. **Capture Image**: Inspectors use the mobile app to take garment images.
2. **Enhance Image**: The image is processed using ESRGAN for clarity.
3. **Analyze Defects**: YOLOv8 detects defects and categorizes them.
4. **Log Details**: The system records defect types, timestamps, and other metadata.
5. **Notify Supervisor**: Flags are raised and displayed on a real-time dashboard for immediate action.
6. **Optimize Processes**: Centralized data provides insights to identify trends and improve production quality.

---

## Hardware Requirements

- **Mobile Devices**: Smartphones or tablets with cameras
- **Edge Computing Devices**: For local processing and real-time decision-making
- **Routers**: Ensure smooth connectivity for data transfer and cloud synchronization

---

## Software Requirements

- **Frameworks**: PyTorch (ML model training), Flutter (mobile app development), Django (backend development)
- **Database**: Cloud-based database system
- **Version Control**: Git (e.g., GitHub) for code management
- **Design Tools**: Figma (for UI/UX design)

---

## System Scope

### In-Scope

- Real-time defect detection and logging
- Mobile-based image capture and processing
- Supervisor dashboard for real-time updates
- Centralized analytics and reporting

### Out-of-Scope

- Physical defect repairs
- Offline usage without internet connectivity
- Predictive maintenance or future defect prediction

---



## Team Members

- **Luckmali Fernando (Group Leader)**
- **Kesara Jayaweera**
- **Hassan Shamil**
- **Anton Luckshman**
- **Judith Nihara**
- **Vanuja Nanayakkara**

---

## Acknowledgements

We extend our gratitude to:

- **Module Leader**: Mr. Banuka Athuraliya for his guidance and support.
- **Mentor**: Ms. Subhaka Bavanishankar for her expert insights and constructive feedback.
- Industry professionals who shared their valuable insights to refine the project.

---


## References

- "What is 7/0 System in Garment Inspection?" (Fantasygameday, 2024)
- "Improved YOLOv8 garment sewing defect detection" (Journal of Measurements in Engineering, 2024)
- "Deep-GD: Deep Learning based Automatic Garment Defect Detection" (International Journal of Electrical and Electronics Research, 2024)
