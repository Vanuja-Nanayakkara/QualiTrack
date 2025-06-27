import React from "react";
import { CheckCircle } from "lucide-react";

export const PricingSection = () => {
  const plans = [
    {
      name: "Starter",
      price: "499",
      description: "Perfect for small manufacturers",
      features: [
        "Up to 1,000 inspections/month",
        "Basic defect detection",
        "Email support",
        "Mobile app access",
        "Basic analytics",
      ],
    },
    {
      name: "Professional",
      price: "999",
      description: "Ideal for medium-sized operations",
      features: [
        "Up to 5,000 inspections/month",
        "Advanced defect detection",
        "Priority support",
        "Real-time notifications",
        "Advanced analytics",
        "API access",
      ],
      popular: true,
    },
    {
      name: "Enterprise",
      price: "Custom",
      description: "For large-scale manufacturing",
      features: [
        "Unlimited inspections",
        "Custom ML model training",
        "24/7 dedicated support",
        "Custom integration",
        "Advanced analytics",
        "Multi-location support",
      ],
    },
  ];

  return (
    <div id="pricing" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Pricing
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Choose the right plan for your needs
          </p>
        </div>

        <div className="mt-16 grid gap-8 lg:grid-cols-3">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`bg-white rounded-lg shadow-lg overflow-hidden
                  ${plan.popular ? "ring-2 ring-blue-600 scale-105" : ""}`}
            >
              {plan.popular && (
                <div className="bg-blue-600 text-white text-center py-2 text-sm font-medium">
                  Most Popular
                </div>
              )}
              <div className="p-8">
                <h3 className="text-2xl font-bold text-gray-900">
                  {plan.name}
                </h3>
                <p className="mt-4 text-gray-500">{plan.description}</p>
                <p className="mt-8">
                  <span className="text-4xl font-extrabold text-gray-900">
                    ${plan.price}
                  </span>
                  <span className="text-gray-500">/month</span>
                </p>
                <ul className="mt-8 space-y-4">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center">
                      <CheckCircle className="h-5 w-5 text-blue-600 mr-2" />
                      <span className="text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
                <button
                  className={`mt-8 w-full py-3 px-4 rounded-md font-medium
                    ${
                      plan.popular
                        ? "bg-blue-600 text-white hover:bg-blue-700"
                        : "bg-gray-100 text-gray-900 hover:bg-gray-200"
                    }`}
                >
                  Get Started
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
