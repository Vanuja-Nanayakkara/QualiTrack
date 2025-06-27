// src/pages/about.tsx
import React from "react";
import { FadeIn, StaggeredList } from "@/animations";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import {
  Linkedin,
  Mail,
  Award,
  BookOpen,
  Users,
  CheckCircle,
} from "lucide-react";
import Image from "next/image";

const AboutUs = () => {
  const teamMembers = [
    {
      name: "Luckmali Fernando",
      role: "Group Leader & Full Stack Developer",
      image: "/Luckmali.jpg",
      uowId: "w2051693",
      iitId: "20230584",
      linkedin: "#",
      email: "luckmali@example.com",
      bio: "As the group leader, Luckmali coordinated the project and contributed to both frontend and backend development. With expertise in React and Django, she ensured the seamless integration of all system components.",
    },
    {
      name: "Kesara Jayaweera",
      role: "ML Engineer &Backend Developer",
      image: "/none.jpg",
      uowId: "w2055564",
      iitId: "20221870",
      linkedin: "#",
      email: "kesara@example.com",
      bio: "Kesara architected the robust Django backend, implementing the RESTful API endpoints and database structure. His expertise in creating scalable server-side solutions was instrumental to the project's success.",
    },
    {
      name: "Hassan Shamil",
      role: "ML Engineer & Frontend Developer",
      image: "/none.jpg",
      uowId: "w2053277",
      iitId: "20222217",
      linkedin: "#",
      email: "hassan@example.com",
      bio: "Hassan developed the machine learning models that power our defect detection system and contributed to the frontend development. His work with YOLOv8 and ESRGAN algorithms enabled the accurate identification of garment defects in real-time.",
    },
    {
      name: "Anton Luckshman",
      role: "ML Engineer & Backend Developer",
      image: "/Luckshman.jpg",
      uowId: "w2082257",
      iitId: "20232578",
      linkedin: "https://www.linkedin.com/in/anton-luckshman-53121a265",
      email: "antonluckshman2@gmail.com",
      bio: "Anton developed the machine learning models and architected the robust Django backend. His work with YOLOv8 and ESRGAN algorithms enabled the accurate identification of garment defects in real-time, and his backend development ensured the seamless integration of all system components.",
    },
    {
      name: "Judith Nihara",
      role: "UI/UX Designer & Frontend Developer",
      image: "/Judith.jpg",
      uowId: "w2051970",
      iitId: "20231188",
      linkedin: "#",
      email: "judith@example.com",
      bio: "Judith designed the intuitive user interfaces and experiences that make our system accessible. Her research-driven approach to UX ensured that the final product met the needs of all stakeholders in the garment inspection process. She also contributed significantly to the frontend development.",
    },
    {
      name: "Vanuja Nanayakkara",
      role: "UI/UX Designer & Frontend Developer",
      image: "/none.jpg",
      uowId: "w2053144",
      iitId: "20221325",
      linkedin: "#",
      email: "vanuja@example.com",
      bio: "Vanuja implemented rigorous testing protocols to ensure the quality and reliability of the system and contributed to the frontend development. His attention to detail and systematic approach to quality assurance resulted in a robust and dependable final product.",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="py-24 px-4 sm:px-6 lg:px-8">
        {" "}
        {/* Increased top padding from py-12 to py-24 */}
        <div className="max-w-7xl mx-auto">
          <FadeIn>
            <div className="text-center  mb-16">
              <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
                About Our Team
              </h1>
              <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
                Meet the talented individuals behind the QualiTrack project, a
                collaboration between Informatics Institute of Technology (IIT)
                Sri Lanka and the University of Westminster, UK.
              </p>
            </div>

            {/* Project Overview */}
            <div className="mb-16 bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Our Mission
              </h2>

              <p className="text-gray-600 mb-8 text-lg leading-relaxed">
                The QualiTrack represents our commitment to revolutionizing
                quality control processes in the garment manufacturing industry.
                As the final project for our Software Development Group Project
                module (5COSC021C), we&apos;ve combined cutting-edge technology
                with deep industry insights to address a critical challenge in
                textile production.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                    <BookOpen className="h-5 w-5 mr-2 text-blue-600" />
                    The Problem We&apos;re Solving
                  </h3>
                  <p className="text-gray-600">
                    Traditional 7/0 inspections in garment manufacturing are
                    manual, time-consuming processes where quality control
                    inspectors examine seven garments at each operator&apos;s
                    workstation. This approach is prone to human error, lacks
                    real-time monitoring capabilities, and cannot effectively
                    track recurring quality issues. The result is production
                    bottlenecks, increased defect rates, and higher costs.
                  </p>
                </div>

                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                    <Award className="h-5 w-5 mr-2 text-blue-600" />
                    Our Innovative Solution
                  </h3>
                  <p className="text-gray-600">
                    We&apos;ve developed an AI-powered inspection system that
                    uses machine learning to detect defects with higher accuracy
                    than human inspectors. Our mobile application allows for
                    real-time image capture and analysis, while super-resolution
                    technology enhances image quality to identify even the
                    smallest defects. The system immediately alerts supervisors
                    to quality issues and provides comprehensive analytics for
                    continuous improvement.
                  </p>
                </div>
              </div>

              <div className="bg-blue-50 p-6 rounded-lg mb-8">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <Users className="h-5 w-5 mr-2 text-blue-600" />
                  Academic Supervision
                </h3>
                <p className="text-gray-600 mb-4">
                  This project was developed under the guidance of our module
                  leader, Mr. Banuka Athuraliya, and our mentor, Ms. Subhaka
                  Bavanishankar, whose expertise and feedback were invaluable to
                  our success. Their direction helped us translate theoretical
                  knowledge into a practical solution with real-world
                  applications.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="flex items-center">
                    <p className="font-medium text-black">
                      Mr. Banuka Athuraliya
                    </p>
                    <div className="text-sm text-gray-500 ml-2">
                      Module Leader
                    </div>
                  </div>
                  <div className="flex items-center">
                    <p className="font-medium text-black">
                      Ms. Subhaka Bavanishankar
                    </p>
                    <div className="text-sm text-gray-500 ml-2">
                      Project Mentor
                    </div>
                  </div>
                </div>
              </div>

              <h3 className="font-semibold text-gray-900 mb-3">
                Project Outcomes
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                <div className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mt-1 mr-2 flex-shrink-0" />
                  <p className="text-gray-600">
                    98% accurate defect detection, compared to 85% with manual
                    inspection
                  </p>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mt-1 mr-2 flex-shrink-0" />
                  <p className="text-gray-600">
                    60% reduction in inspection time, improving overall
                    production efficiency
                  </p>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mt-1 mr-2 flex-shrink-0" />
                  <p className="text-gray-600">
                    45% decrease in defect-related costs through early detection
                    and intervention
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    Technologies Used
                  </h3>
                  <ul className="list-disc list-inside text-gray-600 space-y-2">
                    <li>Machine Learning with YOLOv8 for object detection</li>
                    <li>ESRGAN for super-resolution image enhancement</li>
                    <li>React & Next.js for responsive frontend interfaces</li>
                    <li>Django REST Framework for robust API development</li>
                    <li>WebSockets for real-time notifications</li>
                    <li>TensorFlow & PyTorch for ML model training</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    Key Features
                  </h3>
                  <ul className="list-disc list-inside text-gray-600 space-y-2">
                    <li>AI-powered defect detection with high accuracy</li>
                    <li>Real-time supervisor notifications and alerts</li>
                    <li>Mobile-first approach for on-floor inspection</li>
                    <li>Comprehensive analytics dashboard</li>
                    <li>Automated reporting and data visualization</li>
                    <li>Centralized database for trend analysis</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Team Members */}
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
              Meet Our Team
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto text-center mb-12">
              Our diverse team combines expertise in software development,
              machine learning, design, and quality assurance to create a
              comprehensive solution for the garment industry.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <StaggeredList>
                {teamMembers.map((member, index) => (
                  <div
                    key={index}
                    className="bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-blue-600"
                  >
                    <Image
                      src={member.image}
                      alt={member.name}
                      className="w-full h-50 object-cover object-center"
                      width={300}
                      height={200}
                    />
                    <div className="p-6">
                      <h3 className="text-xl font-bold text-gray-900">
                        {member.name}
                      </h3>
                      <p className="text-blue-600 mb-2">{member.role}</p>
                      <div className="text-sm text-gray-600 mb-4">
                        <p>UoW ID: {member.uowId}</p>
                        <p>IIT ID: {member.iitId}</p>
                      </div>
                      <p className="text-gray-600 mb-4 text-sm">{member.bio}</p>
                      <div className="flex space-x-4">
                        <a
                          href={member.linkedin}
                          className="text-gray-600 hover:text-blue-600 transition-colors"
                          aria-label={`${member.name}'s LinkedIn profile`}
                        >
                          <Linkedin className="h-5 w-5" />
                        </a>
                        <a
                          href={`mailto:${member.email}`}
                          className="text-gray-600 hover:text-blue-600 transition-colors"
                          aria-label={`Email ${member.name}`}
                        >
                          <Mail className="h-5 w-5" />
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </StaggeredList>
            </div>

            {/* Project Timeline */}
            <div className="mt-16 bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Project Timeline
              </h2>
              <div className="space-y-8">
                <div className="relative pl-8 pb-8 border-l-2 border-blue-200">
                  <div className="absolute -left-2 top-0 w-6 h-6 rounded-full bg-blue-600"></div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Project Initiation
                  </h3>
                  <p className="text-gray-600 mb-1">October 2024</p>
                  <p className="text-gray-600">
                    Research, problem identification, and project planning
                  </p>
                </div>

                <div className="relative pl-8 pb-8 border-l-2 border-blue-200">
                  <div className="absolute -left-2 top-0 w-6 h-6 rounded-full bg-blue-600"></div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Design Phase
                  </h3>
                  <p className="text-gray-600 mb-1">November 2024</p>
                  <p className="text-gray-600">
                    System architecture design, UI/UX mockups, and database
                    schema planning
                  </p>
                </div>

                <div className="relative pl-8 pb-8 border-l-2 border-blue-200">
                  <div className="absolute -left-2 top-0 w-6 h-6 rounded-full bg-blue-600"></div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Development Phase
                  </h3>
                  <p className="text-gray-600 mb-1">
                    December 2024 - January 2024
                  </p>
                  <p className="text-gray-600">
                    Implementation of core functionalities, ML model training,
                    and integration
                  </p>
                </div>

                <div className="relative pl-8">
                  <div className="absolute -left-2 top-0 w-6 h-6 rounded-full bg-blue-600"></div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Testing & Refinement
                  </h3>
                  <p className="text-gray-600 mb-1">February 2025 </p>
                  <p className="text-gray-600">
                    Quality assurance, performance optimization, and final
                    deployment
                  </p>
                </div>
              </div>
            </div>
          </FadeIn>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default AboutUs;
