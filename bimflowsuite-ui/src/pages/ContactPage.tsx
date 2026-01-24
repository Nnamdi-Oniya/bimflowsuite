import React, { useState } from "react";
import "../assets/ContactPage.css";
import contactHero from "../assets/images/contactHero.jpg";

const ContactPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    subject: "",
    message: ""
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    alert("Thank you for your message! We'll get back to you soon.");
    setFormData({ name: "", email: "", company: "", subject: "", message: "" });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const contactMethods = [
    {
      icon: "📧",
      title: "Email Us",
      value: "hello@bimflow.dev",
      link: "mailto:hello@bimflow.dev"
    },
    {
      icon: "💬",
      title: "Live Chat",
      value: "Available 9AM-6PM GMT",
      link: "#"
    },
    {
      icon: "📱",
      title: "Social Media",
      value: "@BIMFlowSuite",
      link: "https://twitter.com"
    },
    {
      icon: "🐙",
      title: "GitHub",
      value: "github.com/bimflow",
      link: "https://github.com"
    }
  ];

  const faqs = [
    {
      question: "Is BIMFlow Suite really free?",
      answer: "Yes! BIMFlow Suite is 100% open-source and free to use. No hidden costs, no premium tiers. We believe in democratizing BIM technology for everyone."
    },
    {
      question: "What file formats do you support?",
      answer: "We support IFC 4.0 and IFC 4.3 for import/export, along with BCF for issue validation. We're working on adding support for Revit and other proprietary formats."
    },
    {
      question: "Can I use this for commercial projects?",
      answer: "Absolutely! BIMFlow Suite is licensed under MIT, allowing both personal and commercial use without restrictions."
    },
    {
      question: "Do you offer enterprise support?",
      answer: "Yes, we offer dedicated enterprise support packages including SLAs, custom integrations, and training. Contact us for details."
    }
  ];

  return (
    <div className="app-container">
     
      <main className="main-content" role="main">
        <div className="contact-page">
          {/* Hero */}
          <section 
            className="contact-hero"
            style={{
              backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.6), rgba(42, 36, 32, 0.6)), url(${contactHero})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundAttachment: 'fixed'
            }}
          >
            <div className="contact-hero__overlay"></div>
            <div className="contact-hero__content">
              <h1 className="contact-hero__title">Get in Touch</h1>
              <p className="contact-hero__subtitle">
                Have questions? Want to collaborate? We'd love to hear from you.
                Our team is here to help you succeed with BIMFlow Suite.
              </p>
            </div>
          </section>

          {/* Contact Methods */}
          <section className="contact-methods-section">
            <div className="section-container">
              <div className="contact-methods-grid">
                {contactMethods.map((method, index) => (
                  <a
                    key={index}
                    href={method.link}
                    className="contact-method-card"
                    target={method.link.startsWith('http') ? '_blank' : '_self'}
                    rel="noopener noreferrer"
                  >
                    <div className="method-icon">{method.icon}</div>
                    <h3 className="method-title">{method.title}</h3>
                    <p className="method-value">{method.value}</p>
                  </a>
                ))}
              </div>
            </div>
          </section>

          {/* Contact Form */}
          <section className="contact-form-section">
            <div className="section-container">
              <div className="form-layout">
                <div className="form-info">
                  <h2 className="form-info__title">Send Us a Message</h2>
                  <p className="form-info__text">
                    Fill out the form and our team will get back to you within 24 hours.
                    For urgent inquiries, please use our live chat or email directly.
                  </p>
                  <div className="form-info__features">
                    <div className="info-feature">
                      <span className="feature-icon">⚡</span>
                      <div>
                        <h4>Quick Response</h4>
                        <p>Average response time: 4 hours</p>
                      </div>
                    </div>
                    <div className="info-feature">
                      <span className="feature-icon">🔒</span>
                      <div>
                        <h4>Secure & Private</h4>
                        <p>Your data is encrypted and protected</p>
                      </div>
                    </div>
                    <div className="info-feature">
                      <span className="feature-icon">🌍</span>
                      <div>
                        <h4>Global Support</h4>
                        <p>Available in multiple time zones</p>
                      </div>
                    </div>
                  </div>
                </div>

                <form className="contact-form" onSubmit={handleSubmit}>
                  <div className="form-group">
                    <label htmlFor="name">Full Name *</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      placeholder="John Doe"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="email">Email Address *</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      placeholder="john@company.com"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="company">Company Name</label>
                    <input
                      type="text"
                      id="company"
                      name="company"
                      value={formData.company}
                      onChange={handleChange}
                      placeholder="Your Company Ltd."
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="subject">Subject *</label>
                    <select
                      id="subject"
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      required
                    >
                      <option value="">Select a subject</option>
                      <option value="general">General Inquiry</option>
                      <option value="support">Technical Support</option>
                      <option value="partnership">Partnership Opportunity</option>
                      <option value="enterprise">Enterprise Solutions</option>
                      <option value="feedback">Feedback & Suggestions</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="message">Message *</label>
                    <textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      required
                      rows={6}
                      placeholder="Tell us how we can help you..."
                    />
                  </div>

                  <button type="submit" className="form-submit-btn">
                    Send Message
                  </button>
                </form>
              </div>
            </div>
          </section>

          {/* FAQs */}
          <section className="faq-section">
            <div className="section-container">
              <div className="section-header">
                <h2 className="section-title">Frequently Asked Questions</h2>
                <p className="section-subtitle">
                  Quick answers to common questions
                </p>
              </div>
              <div className="faq-grid">
                {faqs.map((faq, index) => (
                  <div key={index} className="faq-item">
                    <h3 className="faq-question">{faq.question}</h3>
                    <p className="faq-answer">{faq.answer}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Map/Location */}
          <section className="location-section">
            <div className="location-container">
              <div className="location-info">
                <h2>Our Global Presence</h2>
                <p>
                  While BIMFlow Suite is a fully remote, open-source project with 
                  contributors worldwide, our core team is based in multiple locations 
                  to provide 24/7 support.
                </p>
                <div className="location-details">
                  <div className="location-item">
                    <span className="location-icon">🌍</span>
                    <div>
                      <h4>Global Community</h4>
                      <p>Contributors from 15+ countries</p>
                    </div>
                  </div>
                  <div className="location-item">
                    <span className="location-icon">⏰</span>
                    <div>
                      <h4>24/7 Availability</h4>
                      <p>Support across all time zones</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="location-map">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d193595.9147703055!2d-74.119763973046!3d40.69740344223377!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c24fa5d33f083b%3A0xc80b8f06e177fe62!2sNew%20York%2C%20NY%2C%20USA!5e0!3m2!1sen!2sus!4v1572911205687!5m2!1sen!2sus"
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen={true}
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Google Map"
                ></iframe>
              </div>
            </div>
          </section>
        </div>
      </main>
     
    </div>
  );
};

export default ContactPage;