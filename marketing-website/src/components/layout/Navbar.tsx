import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { NavLink } from "./NavLink";
import Image from "next/image";
import { User, LogOut, Menu, X } from "lucide-react";
import { SignInModal } from "../auth/SignInModal";
import { SignUpModal } from "../auth/SignUpModal";
import { useAuth } from "../../contexts/AuthContext";

export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isSignInOpen, setIsSignInOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const router = useRouter();
  const { currentUser, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu when route changes
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [router.pathname]);

  const handleGetStartedClick = () => {
    if (currentUser) {
      router.push("/dashboard");
    } else {
      setIsSignUpOpen(true);
    }
  };

  const handleLoginClick = () => {
    setIsSignInOpen(true);
  };

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/");
    } catch (error) {
      console.error("Failed to log out", error);
    }
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <>
      <nav
        className={`fixed w-full z-40 transition-all duration-300 ${
          isScrolled || mobileMenuOpen ? "bg-white shadow-lg" : "bg-transparent"
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex-shrink-0 flex items-center">
              <Link href="/">
                <div className="flex items-center">
                  <Image
                    src="/Logo.png"
                    alt="QualiTrack"
                    className="h-8 w-auto"
                    width={32}
                    height={32}
                  />
                  <span className="ml-2 text-xl font-bold text-blue-600">
                    QualiTrack
                  </span>
                </div>
              </Link>
            </div>

            {/* Mobile menu button */}
            <div className="flex items-center sm:hidden">
              <button
                onClick={toggleMobileMenu}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-600"
                aria-expanded="false"
              >
                <span className="sr-only">Open main menu</span>
                {mobileMenuOpen ? (
                  <X className="block h-6 w-6" aria-hidden="true" />
                ) : (
                  <Menu className="block h-6 w-6" aria-hidden="true" />
                )}
              </button>
            </div>

            {/* Desktop navigation */}
            <div className="hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8">
              <NavLink href="/#features">
                <span className="text-gray-900 hover:text-blue-600">
                  Features
                </span>
              </NavLink>
              <NavLink href="/#how-it-works">
                <span className="text-gray-900 hover:text-blue-600">
                  How it Works
                </span>
              </NavLink>
              <NavLink href="/#testimonials">
                <span className="text-gray-900 hover:text-blue-600">
                  Testimonials
                </span>
              </NavLink>
              <NavLink href="/about">
                <span className="text-gray-900 hover:text-blue-600">
                  About Us
                </span>
              </NavLink>

              {currentUser ? (
                <>
                  <Link href="/dashboard">
                    <span className="text-gray-900 hover:text-blue-600 cursor-pointer">
                      Dashboard
                    </span>
                  </Link>
                  <button
                    className="bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700 transition-colors flex items-center"
                    onClick={handleLogout}
                  >
                    <LogOut className="h-5 w-5 mr-2" />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  {/* Login Button */}
                  <button
                    className="bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700 transition-colors flex items-center"
                    onClick={handleLoginClick}
                  >
                    <User className="h-5 w-5 mr-2" />
                    Login
                  </button>

                  <button
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                    onClick={handleGetStartedClick}
                  >
                    Get Started
                  </button>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Mobile menu, show/hide based on menu state */}
        <div className={`${mobileMenuOpen ? "block" : "hidden"} sm:hidden`}>
          <div className="pt-2 pb-3 space-y-1 bg-white">
            <Link href="/#features">
              <div className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 hover:border-blue-300">
                Features
              </div>
            </Link>
            <Link href="/#how-it-works">
              <div className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 hover:border-blue-300">
                How it Works
              </div>
            </Link>
            <Link href="/#testimonials">
              <div className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 hover:border-blue-300">
                Testimonials
              </div>
            </Link>
            <Link href="/about">
              <div className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 hover:border-blue-300">
                About Us
              </div>
            </Link>
            {currentUser && (
              <Link href="/dashboard">
                <div className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 hover:border-blue-300">
                  Dashboard
                </div>
              </Link>
            )}
          </div>

          {/* Mobile Authentication Buttons */}
          <div className="pt-4 pb-3 border-t border-gray-200 bg-white">
            <div className="flex items-center px-4 space-x-3">
              {currentUser ? (
                <button
                  className="bg-emerald-600 text-white px-4 py-2 w-full rounded-md hover:bg-emerald-700 transition-colors flex items-center justify-center"
                  onClick={handleLogout}
                >
                  <LogOut className="h-5 w-5 mr-2" />
                  Logout
                </button>
              ) : (
                <>
                  <button
                    className="bg-emerald-600 text-white px-4 py-2 flex-1 rounded-md hover:bg-emerald-700 transition-colors flex items-center justify-center"
                    onClick={handleLoginClick}
                  >
                    <User className="h-5 w-5 mr-2" />
                    Login
                  </button>
                  <button
                    className="bg-blue-600 text-white px-4 py-2 flex-1 rounded-md hover:bg-blue-700 transition-colors"
                    onClick={handleGetStartedClick}
                  >
                    Get Started
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Auth Modals */}
      <SignInModal
        isOpen={isSignInOpen}
        onClose={() => setIsSignInOpen(false)}
        onSignUp={() => {
          setIsSignInOpen(false);
          setIsSignUpOpen(true);
        }}
      />

      <SignUpModal
        isOpen={isSignUpOpen}
        onClose={() => setIsSignUpOpen(false)}
        onSignIn={() => {
          setIsSignUpOpen(false);
          setIsSignInOpen(true);
        }}
      />
    </>
  );
};
