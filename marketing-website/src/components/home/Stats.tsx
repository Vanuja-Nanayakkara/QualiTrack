import React from "react";

export const Stats = () => {
  const stats = [
    { number: "98%", label: "Detection Accuracy" },
    { number: "60%", label: "Faster Inspections" },
    { number: "45%", label: "Reduced Defects" },
    { number: "30%", label: "Cost Savings" },
  ];

  return (
    <div className="bg-blue-600">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:py-16 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <p className="text-5xl font-extrabold text-white">
                {stat.number}
              </p>
              <p className="mt-2 text-lg font-medium text-blue-100">
                {stat.label}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
