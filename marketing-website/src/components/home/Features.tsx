import React from "react";
import { Eye, Zap, BarChart2, Shield } from "lucide-react";

export const Features = () => {
  const features = [
    {
      icon: <Eye className="h-6 w-6" />,
      title: "AI-Powered Detection",
      description:
        "Advanced machine learning algorithms detect even the smallest defects with high accuracy.",
    },
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Real-time Processing",
      description:
        "Instant analysis and notifications enable immediate corrective actions.",
    },
    {
      icon: <BarChart2 className="h-6 w-6" />,
      title: "Comprehensive Analytics",
      description:
        "Detailed insights and trends to optimize your quality control process.",
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Quality Assurance",
      description:
        "Maintain consistent quality standards across your production line.",
    },
  ];

  return (
    <div id="features" className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Features
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need for perfect quality control
          </p>
        </div>

        <div className="mt-10">
          <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            {features.map((feature, index) => (
              <div key={index} className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                  {feature.icon}
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">
                  {feature.title}
                </p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
