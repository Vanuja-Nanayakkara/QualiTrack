import React from "react";

export const HowItWorks = () => {
  const steps = [
    {
      number: "01",
      title: "Capture",
      description: "Take photos of garments using our mobile app",
    },
    {
      number: "02",
      title: "Analyze",
      description: "AI instantly processes images to detect defects",
    },
    {
      number: "03",
      title: "Alert",
      description: "Real-time notifications for any quality issues",
    },
    {
      number: "04",
      title: "Track",
      description: "Monitor trends and optimize your process",
    },
  ];

  return (
    <div id="how-it-works" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            How It Works
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Simple and effective quality control
          </p>
        </div>

        <div className="mt-16">
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
            {steps.map((step, index) => (
              <div
                key={index}
                className="relative bg-white p-6 rounded-lg shadow-lg"
              >
                <div className="text-blue-600 text-4xl font-bold mb-4">
                  {step.number}
                </div>
                <h3 className="text-lg font-medium text-gray-900">
                  {step.title}
                </h3>
                <p className="mt-2 text-base text-gray-500">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
