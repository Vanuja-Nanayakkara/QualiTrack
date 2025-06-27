import React from "react";

export const Testimonials = () => {
  const testimonials = [
    {
      quote:
        "This system has transformed our quality control process. We&apos;ve seen significant improvements in efficiency and accuracy.",
      author: "Sarah Chen",
      role: "Quality Manager",
      company: "Fashion Dynamics",
    },
    {
      quote:
        "The real-time alerts and analytics have helped us reduce defects by 45%. Amazing results!",
      author: "Michael Rodriguez",
      role: "Production Head",
      company: "Garment Solutions Inc.",
    },
  ];

  return (
    <div id="testimonials" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Testimonials
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Trusted by industry leaders
          </p>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-2">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-8">
              <div className="text-gray-600 italic">
                &quot;{testimonial.quote}&quot;
              </div>
              <div className="mt-4">
                <p className="text-gray-900 font-medium">
                  {testimonial.author}
                </p>
                <p className="text-gray-500">
                  {testimonial.role}, {testimonial.company}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
