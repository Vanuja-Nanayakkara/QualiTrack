import React from "react";

interface NavLinkProps {
  href: string;
  children: React.ReactNode;
}

export const NavLink = ({ href, children }: NavLinkProps) => (
  <a
    href={href}
    className="text-gray-600 hover:text-gray-900 transition-colors"
  >
    {children}
  </a>
);
