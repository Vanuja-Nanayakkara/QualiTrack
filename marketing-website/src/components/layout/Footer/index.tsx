import React from "react";
import { Eye, Facebook, Twitter, Linkedin, Instagram } from "lucide-react";
import { SocialIcon } from "./SocialIcon";
import { FooterLink } from "./FooterLink";

export const Footer = () => {
  return (
    <footer className="bg-gray-900">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center">
              <Eye className="h-8 w-8 text-blue-500" />
              <span className="ml-2 text-xl font-bold text-white">
                QualiTrack
              </span>
            </div>
            <p className="mt-4 text-gray-400 max-w-md">
              Revolutionizing garment manufacturing with AI-powered quality
              control. Detect defects in real-time and improve production
              efficiency.
            </p>
            <div className="mt-6 flex space-x-6">
              <SocialIcon icon={<Facebook />} href="#" />
              <SocialIcon icon={<Twitter />} href="#" />
              <SocialIcon icon={<Linkedin />} href="#" />
              <SocialIcon icon={<Instagram />} href="#" />
            </div>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Product</h3>
            <ul className="space-y-3">
              <FooterLink href="#features">Features</FooterLink>
              <FooterLink href="#pricing">Pricing</FooterLink>
              <FooterLink href="#how-it-works">How it Works</FooterLink>
              <FooterLink href="#contact">Contact</FooterLink>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Company</h3>
            <ul className="space-y-3">
              <FooterLink href="/about">About Us</FooterLink>
              <FooterLink href="/careers">Careers</FooterLink>
              <FooterLink href="/blog">Blog</FooterLink>
              <FooterLink href="/privacy">Privacy Policy</FooterLink>
              <FooterLink href="/terms">Terms of Service</FooterLink>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800">
          <p className="text-gray-400 text-center">
            © {new Date().getFullYear()} QualiTrack. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
