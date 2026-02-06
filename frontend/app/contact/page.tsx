"use client";

import { useState } from "react";

export default function Contact() {
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        the_email: "", // message
        company: "", // honeypot
    });
    const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (formData.the_email.trim().length < 10) {
            setStatus("error");
            return;
        }

        setStatus("submitting");

        try {
            const res = await fetch("/send_email", {
                method: "POST",
                headers: { "Content-Type": "application/json", Accept: "application/json" },
                body: JSON.stringify(formData),
            });

            const data = await res.json().catch(() => ({ ok: false }));

            if (res.ok && data.ok) {
                setStatus("success");
                setFormData({
                    firstName: "",
                    lastName: "",
                    email: "",
                    the_email: "",
                    company: "",
                });
            } else {
                setStatus("error");
            }
        } catch {
            setStatus("error");
        }
    };

    return (
        <>
            <main className="contact-hero py-5">
                <div className="container">
                    <div className="row justify-content-center text-center mb-4">
                        <div className="col-lg-8">
                            <h1 className="display-5 fw-semibold">Let&apos;s Connect</h1>
                            <p className="lead text-secondary">
                                I&apos;m happy to hear from you. Reach out on social, or drop a message and I&apos;ll reply soon.
                            </p>
                        </div>
                    </div>

                    <div className="row g-4 align-items-stretch">
                        {/* Social links */}
                        <div className="col-12 col-lg-5">
                            <div className="card h-100 shadow-sm border-0 rounded-4 overflow-hidden">
                                <div className="card-body p-4 p-md-5">
                                    <h2 className="h4 mb-4">Social</h2>
                                    <div className="list-group list-group-flush gap-3">
                                        <a
                                            className="list-group-item list-group-item-action d-flex align-items-center rounded-3"
                                            href="https://twitter.com/maelmaitre/"
                                            target="_blank"
                                        >
                                            <img src="/assets/images/twitter.png" className="me-3 contact-icon" alt="Twitter" />
                                            <div>
                                                <div className="fw-semibold">Twitter</div>
                                                <small className="text-secondary">@maelmaitre</small>
                                            </div>
                                        </a>
                                        <a
                                            className="list-group-item list-group-item-action d-flex align-items-center rounded-3"
                                            href="https://www.linkedin.com/in/ma%C3%ABl-ma%C3%AEtre-9318a983/"
                                            target="_blank"
                                        >
                                            <img src="/assets/images/linkedin.svg" className="me-3 contact-icon" alt="LinkedIn" />
                                            <div>
                                                <div className="fw-semibold">LinkedIn</div>
                                                <small className="text-secondary">Professional profile</small>
                                            </div>
                                        </a>
                                        <a
                                            className="list-group-item list-group-item-action d-flex align-items-center rounded-3"
                                            href="https://www.facebook.com/hackerhaiti/"
                                            target="_blank"
                                        >
                                            <img src="/assets/images/facebook.png" className="me-3 contact-icon" alt="Facebook" />
                                            <div>
                                                <div className="fw-semibold">Facebook</div>
                                                <small className="text-secondary">/hackerhaiti</small>
                                            </div>
                                        </a>
                                        <a
                                            className="list-group-item list-group-item-action d-flex align-items-center rounded-3"
                                            href="https://www.instagram.com/maymaitre/"
                                            target="_blank"
                                        >
                                            <img
                                                src="/assets/images/instagram.jpg"
                                                className="me-3 contact-icon contact-icon--round"
                                                alt="Instagram"
                                            />
                                            <div>
                                                <div className="fw-semibold">Instagram</div>
                                                <small className="text-secondary">@maymaitre</small>
                                            </div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Contact form */}
                        <div className="col-12 col-lg-7">
                            <div className="card h-100 shadow-sm border-0 rounded-4">
                                <div className="card-body p-4 p-md-5">
                                    <div className="d-flex align-items-center mb-3">
                                        <img src="/assets/images/email.png" width="36" height="32" className="me-2" alt="Email" />
                                        <h2 className="h4 mb-0">Send me a message</h2>
                                    </div>

                                    <form id="contactForm" onSubmit={handleSubmit} noValidate>
                                        {/* Honeypot anti-bot field (hidden) */}
                                        <input
                                            type="text"
                                            name="company"
                                            id="company"
                                            className="d-none"
                                            autoComplete="off"
                                            tabIndex={-1}
                                            value={formData.company}
                                            onChange={handleChange}
                                        />

                                        <div className="row g-3">
                                            <div className="col-md-6">
                                                <div className="form-floating">
                                                    <input
                                                        type="text"
                                                        className="form-control"
                                                        id="firstName"
                                                        name="firstName"
                                                        placeholder="First name"
                                                        required
                                                        value={formData.firstName}
                                                        onChange={handleChange}
                                                    />
                                                    <label htmlFor="firstName">First name</label>
                                                </div>
                                            </div>
                                            <div className="col-md-6">
                                                <div className="form-floating">
                                                    <input
                                                        type="text"
                                                        className="form-control"
                                                        id="lastName"
                                                        name="lastName"
                                                        placeholder="Last name"
                                                        required
                                                        value={formData.lastName}
                                                        onChange={handleChange}
                                                    />
                                                    <label htmlFor="lastName">Last name</label>
                                                </div>
                                            </div>
                                            <div className="col-12">
                                                <div className="form-floating">
                                                    <input
                                                        type="email"
                                                        className="form-control"
                                                        id="email"
                                                        name="email"
                                                        placeholder="name@example.com"
                                                        required
                                                        value={formData.email}
                                                        onChange={handleChange}
                                                    />
                                                    <label htmlFor="email">Email</label>
                                                </div>
                                            </div>
                                            <div className="col-12">
                                                <div className="form-floating">
                                                    <textarea
                                                        className="form-control"
                                                        placeholder="Write your message"
                                                        id="the_email"
                                                        name="the_email"
                                                        style={{ height: "140px" }}
                                                        required
                                                        value={formData.the_email}
                                                        onChange={handleChange}
                                                    ></textarea>
                                                    <label htmlFor="the_email">Message</label>
                                                </div>
                                                <div className="form-text text-secondary">Be specific. Min 10 characters.</div>
                                            </div>
                                            <div className="col-12 d-grid">
                                                <button
                                                    id="submitBtn"
                                                    className="btn btn-primary btn-lg rounded-3"
                                                    type="submit"
                                                    disabled={status === "submitting"}
                                                >
                                                    {status === "submitting" && (
                                                        <span
                                                            className="spinner-border spinner-border-sm me-2"
                                                            role="status"
                                                            aria-hidden="true"
                                                            id="btnSpinner"
                                                        ></span>
                                                    )}
                                                    Send message
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Toast */}
            <div className="position-fixed top-0 start-50 translate-middle-x p-3" style={{ zIndex: 1080 }}>
                {status === "success" && (
                    <div
                        id="contactToast"
                        className="toast align-items-center text-bg-success border-0 show"
                        role="alert"
                        aria-live="assertive"
                        aria-atomic="true"
                    >
                        <div className="d-flex">
                            <div className="toast-body">Message sent successfully. I&apos;ll be in touch!</div>
                            <button
                                type="button"
                                className="btn-close btn-close-white me-2 m-auto"
                                onClick={() => setStatus("idle")}
                                aria-label="Close"
                            ></button>
                        </div>
                    </div>
                )}
                {status === "error" && (
                    <div
                        id="contactToastError"
                        className="toast align-items-center text-bg-danger border-0 mt-2 show"
                        role="alert"
                        aria-live="assertive"
                        aria-atomic="true"
                    >
                        <div className="d-flex">
                            <div className="toast-body">Could not send your message. Please try again.</div>
                            <button
                                type="button"
                                className="btn-close btn-close-white me-2 m-auto"
                                onClick={() => setStatus("idle")}
                                aria-label="Close"
                            ></button>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
