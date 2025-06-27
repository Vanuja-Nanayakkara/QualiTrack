export interface Testimonial {
  quote: string;
  author: string;
  role: string;
  company: string;
}

export interface Feature {
  icon: React.ReactNode;
  title: string;
  description: string;
}

export interface Step {
  number: string;
  title: string;
  description: string;
}

export interface Stat {
  number: string;
  label: string;
}

export interface Plan {
  name: string;
  price: string;
  description: string;
  features: string[];
  popular?: boolean;
}

export interface FormData {
  name: string;
  email: string;
  company: string;
  message: string;
}
