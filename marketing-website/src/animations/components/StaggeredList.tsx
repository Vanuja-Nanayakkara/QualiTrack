import React from "react";
import { FadeIn } from "./FadeIn";

interface StaggeredListProps {
  children: React.ReactNode[];
  staggerDelay?: number;
}

export const StaggeredList: React.FC<StaggeredListProps> = ({
  children,
  staggerDelay = 100,
}) => {
  return (
    <>
      {React.Children.map(children, (child, index) => (
        <FadeIn delay={index * staggerDelay}>{child}</FadeIn>
      ))}
    </>
  );
};
