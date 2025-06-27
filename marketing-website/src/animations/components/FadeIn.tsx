import React, { useEffect, useRef, useState } from "react";

interface FadeInProps {
  children: React.ReactNode;
  delay?: number;
  direction?: "up" | "down" | "left" | "right";
}

export const FadeIn: React.FC<FadeInProps> = ({
  children,
  delay = 0,
  direction = "up",
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const currentElement = elementRef.current;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(entry.target);
        }
      },
      {
        threshold: 0.1,
      }
    );

    if (currentElement) {
      observer.observe(currentElement);
    }

    return () => {
      if (currentElement) {
        observer.unobserve(currentElement);
      }
    };
  }, []);

  const getAnimationClass = () => {
    switch (direction) {
      case "up":
        return "animate-fade-in-up";
      case "down":
        return "animate-fade-in-down";
      case "left":
        return "animate-fade-in-left";
      case "right":
        return "animate-fade-in-right";
      default:
        return "animate-fade-in-up";
    }
  };

  return (
    <div
      ref={elementRef}
      className={`opacity-0 ${isVisible ? getAnimationClass() : ""}`}
      style={{
        animationDelay: `${delay}ms`,
        animationFillMode: "forwards",
      }}
    >
      {children}
    </div>
  );
};
