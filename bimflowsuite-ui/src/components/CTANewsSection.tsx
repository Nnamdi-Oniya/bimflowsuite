// src/components/CTANewsSection.tsx – 100% COMPLETE WITH BEAUTIFUL 3D FAQ
import React, { useState } from "react";
import GetStartedModal from "./GetStartedModal";
import "../assets/CTANewsSection.css";

const CTANewsSection: React.FC = () => {
  const [isGetStartedModalOpen, setIsGetStartedModalOpen] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const toggleFaq = (index: number) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  const faqs = [
    {
      q: "What is BIMFlow Suite?",
      a: "BIMFlow Suite is an open-source platform that automates BIM workflows for SMEs. It generates IFC 4.3 compliant models for buildings, bridges, roads and high-rises from simple inputs — no expensive software or BIM expertise required."
    },
    {
      q: "Do I need BIM expertise to use it?",
      a: "No. You describe your project in plain language or fill a simple form. Our parametric engine creates a fully compliant 3D model, validates it, runs compliance checks, calculates quantities, estimates costs and generates a Gantt schedule — all automatically."
    },
    {
      q: "Which file formats are supported?",
      a: "We fully support IFC 4.3 (primary), IFC4 and IFC2x3. Upload your existing IFC file or let us generate a new one from scratch. All outputs are 100% open standard compliant."
    },
    {
      q: "How fast is the processing?",
      a: "IFC files up to 100 MB are processed in under 60 seconds. Model generation from intent, validation, clash detection, compliance checks, QTO, cost estimation and Gantt creation happen instantly."
    },
    {
      q: "Is it really free and open-source?",
      a: "Yes, 100% free and fully open-source. Use it commercially, modify it, contribute — everything is on GitHub under permissive licenses. No subscriptions, no hidden costs."
    },
    {
      q: "What types of projects can I create?",
      a: "Buildings (residential, commercial, healthcare, educational), bridges, roads, high-rises and any custom infrastructure. Our asset packs cover BuildingPack, BridgePack, RoadPack and HighRisePack."
    },
    {
      q: "Can I download reports?",
      a: "Absolutely. Get PDF summaries, CSV/JSON data exports, BCF clash reports and interactive Gantt charts — all downloadable in one click."
    },
    {
      q: "Is my data secure?",
      a: "Yes. Files are processed securely and deleted after analysis unless you save the project. We follow OAuth 2.1, encrypted storage and strict data validation."
    }
  ];

  return (
    <>
      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-section__overlay"></div>
        <div className="cta-section__container">
          <div className="cta-section__content">
            <h2 className="cta-section__title">Ready to Automate Your BIM Workflow?</h2>
            <p className="cta-section__text">
              Join thousands of SMEs already saving time and money with open-source BIM automation.
            </p>
            <button className="cta-section__btn" onClick={() => setIsGetStartedModalOpen(true)}>
              Get Started — It's Free
            </button>
          </div>
        </div>
      </section>

      {/* FAQ Section – Beautiful 3D Card Style */}
      {/* ADDED: id="faq-section" to make it targetable by the URL hash */}
      <section id="faq-section" className="faq-section"> 
        <div className="faq-section__container">
          <h2 className="faq-section__title">Frequently Asked Questions</h2>
          <p className="faq-section__subtitle">
            Everything you need to know about BIMFlow Suite
          </p>

          <div className="faq-grid">
            {faqs.map((faq, index) => (
              <div
                key={index}
                className={`faq-card ${openFaq === index ? "faq-card--open" : ""}`}
                onClick={() => toggleFaq(index)}
              >
                <div className="faq-card__header">
                  <h3 className="faq-card__question">{faq.q}</h3>
                  <span className="faq-card__toggle">
                    {openFaq === index ? "−" : "+"}
                  </span>
                </div>
                <div className="faq-card__answer">
                  <p>{faq.a}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Latest News Section – Kept minimal as requested */}
      <section className="latest-news">
        <div className="latest-news__container">
          <h2 className="latest-news__title">Latest Updates</h2>
          <div className="latest-news__grid">
            <div className="latest-news__card">
              <div className="latest-news__date">
                <span className="latest-news__day">18</span>
                <span className="latest-news__month">NOV</span>
              </div>
              <div className="latest-news__content">
                <h3 className="latest-news__heading">BIMFlow Suite v1.2 Released</h3>
                <p className="latest-news__excerpt">
                  Full IFC 4.3 support, bridge & road asset packs, and enhanced compliance engine now live.
                </p>
              </div>
            </div>
            <div className="latest-news__card">
              <div className="latest-news__date">
                <span className="latest-news__day">05</span>
                <span className="latest-news__month">NOV</span>
              </div>
              <div className="latest-news__content">
                <h3 className="latest-news__heading">50+ GitHub Stars Achieved</h3>
                <p className="latest-news__excerpt">
                  The community is growing fast — thank you for your support and contributions!
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <GetStartedModal
        isOpen={isGetStartedModalOpen}
        onClose={() => setIsGetStartedModalOpen(false)}
      />
    </>
  );
};

export default CTANewsSection;