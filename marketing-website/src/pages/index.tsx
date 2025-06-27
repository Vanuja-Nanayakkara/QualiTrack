import React from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Hero } from "@/components/home/Hero";
import { Features } from "@/components/home/Features";
import { HowItWorks } from "@/components/home/HowItWorks";
import { Stats } from "@/components/home/Stats";
import { PricingSection } from "@/components/home/Pricing";
import { Testimonials } from "@/components/home/Testimonials";
import { ContactForm } from "@/components/home/ContactForm";
import { CallToAction } from "@/components/home/CallToAction";
import { Footer } from "@/components/layout/Footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <Stats />
      <PricingSection />
      <Testimonials />
      <ContactForm />
      <CallToAction />
      <Footer />
    </div>
  );
}
