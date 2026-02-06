import type { NextConfig } from "next";

const backendBaseUrl = (process.env.BACKEND_URL || "http://127.0.0.1:5000").replace(/\/+$/, "");

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/send_email",
        destination: `${backendBaseUrl}/send_email`,
      },
    ];
  },
};

export default nextConfig;
