// src/pages/get-started.tsx
import React, { useState } from "react";
import { CheckCircle, ArrowRight } from "lucide-react";
import { FadeIn } from "@/animations";

const GetStarted = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    companyName: "",
    industry: "",
    size: "",
    email: "",
    phone: "",
    requirements: "",
  });

  const steps = [
    { number: 1, title: "Company Information" },
    { number: 2, title: "Contact Details" },
    { number: 3, title: "Requirements" },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (step < 3) {
      setStep(step + 1);
    } else {
      // Handle form submission
      console.log("Form submitted:", formData);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <FadeIn>
          <div className="text-center mb-12">
            <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Get Started with 7/0 Inspector
            </h1>
            <p className="mt-4 text-lg text-gray-600">
              Complete the following steps to begin your quality inspection
              journey
            </p>
          </div>

          {/* Progress Steps */}
          <div className="mb-8">
            <div className="flex justify-between">
              {steps.map((s) => (
                <div
                  key={s.number}
                  className={`flex items-center ${
                    step >= s.number ? "text-blue-600" : "text-gray-400"
                  }`}
                >
                  <div
                    className={`
                    flex items-center justify-center w-8 h-8 rounded-full border-2
                    ${
                      step >= s.number
                        ? "border-blue-600 bg-blue-50"
                        : "border-gray-300"
                    }
                  `}
                  >
                    {step > s.number ? (
                      <CheckCircle className="w-5 h-5" />
                    ) : (
                      <span>{s.number}</span>
                    )}
                  </div>
                  <span className="ml-2 text-sm font-medium">{s.title}</span>
                  {s.number < steps.length && (
                    <ArrowRight className="w-5 h-5 mx-4" />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Form */}
          <form
            onSubmit={handleSubmit}
            className="space-y-6 bg-blue-100 p-8 rounded-lg shadow"
          >
            {step === 1 && (
              <div className="space-y-6">
                <div>
                  <label
                    htmlFor="companyName"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="companyName"
                    value={formData.companyName}
                    onChange={(e) =>
                      setFormData({ ...formData, companyName: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-black"
                    required
                  />
                </div>
                <div>
                  <label
                    htmlFor="industry"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Industry
                  </label>
                  <select
                    id="industry"
                    value={formData.industry}
                    onChange={(e) =>
                      setFormData({ ...formData, industry: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-black"
                    required
                  >
                    <option value="">Select Industry</option>
                    <option value="apparel">Apparel Manufacturing</option>
                    <option value="textile">Textile Production</option>
                    <option value="fashion">Fashion & Accessories</option>
                  </select>
                </div>
                <div>
                  <label
                    htmlFor="size"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Company Size
                  </label>
                  <select
                    id="size"
                    value={formData.size}
                    onChange={(e) =>
                      setFormData({ ...formData, size: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-black"
                    required
                  >
                    <option value="">Select Size</option>
                    <option value="small">Small (1-50 employees)</option>
                    <option value="medium">Medium (51-200 employees)</option>
                    <option value="large">Large (201+ employees)</option>
                  </select>
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-6">
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={formData.email}
                    onChange={(e) =>
                      setFormData({ ...formData, email: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label
                    htmlFor="phone"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    value={formData.phone}
                    onChange={(e) =>
                      setFormData({ ...formData, phone: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
            )}

            {step === 3 && (
              <div>
                <label
                  htmlFor="requirements"
                  className="block text-sm font-medium text-gray-700"
                >
                  Specific Requirements
                </label>
                <textarea
                  id="requirements"
                  rows={4}
                  value={formData.requirements}
                  onChange={(e) =>
                    setFormData({ ...formData, requirements: e.target.value })
                  }
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="Tell us about your quality inspection needs..."
                  required
                />
              </div>
            )}

            <div className="flex justify-between pt-4">
              {step > 1 && (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="bg-gray-100 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-200"
                >
                  Back
                </button>
              )}
              <button
                type="submit"
                className="ml-auto bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
              >
                {step === 3 ? "Submit" : "Next"}
              </button>
            </div>
          </form>
        </FadeIn>
      </div>
    </div>
  );
};

export default GetStarted;
