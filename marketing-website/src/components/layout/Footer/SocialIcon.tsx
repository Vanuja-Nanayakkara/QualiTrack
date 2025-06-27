import React from "react";

interface SocialIconProps {
  icon: React.ReactNode;
  href: string;
}

export const SocialIcon = ({ icon, href }: SocialIconProps) => (
  <a
    href={href}
    className="text-gray-400 hover:text-gray-300 transition-colors"
  >
    {icon}
  </a>
);
