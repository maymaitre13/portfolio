import Link from "next/link";

export const metadata = {
  title: "Maël Maître",
};

export default function Home() {
  return (
    <div id="wrapper">
      {/* Nav */}
      <nav id="nav">
        <Link href="#" className="icon solid fa-home">
          <span>Home</span>
        </Link>
        <Link href="#work" className="icon solid fa-folder">
          <span>Skills</span>
        </Link>
        <Link href="#tools" className="icon solid fa-wrench">
          <span>Project/Tools</span>
        </Link>
        <Link href="/contact" className="icon solid fa-comments">
          <span>Contact</span>
        </Link>
      </nav>

      {/* Main */}
      <div id="main">
        {/* Me */}
        <article id="home" className="panel intro">
          <header>
            <div className="about-me__info--para buttom">
              <h2 className="about-me__info--title buttom">
                Hey, I&apos;m Maël Maître
              </h2>
              <br />
              Telecom professional with over a decade of experience since{" "}
              <time dateTime="2012">2012</time>. Experienced{" "}
              <strong>NOC Engineer</strong> and{" "}
              <strong>Network Management System Engineer</strong> with strong
              skills in <strong>Network Administration</strong> and{" "}
              <strong>Coding</strong>. Holder of a Computer Science degree from{" "}
              <b>INUKA / UQAM</b>.
            </div>
          </header>
          <a href="#work" className="jumplink pic">
            <img src="/assets/images/mael.png" alt="" />
          </a>
        </article>

        {/* Work */}
        <article id="work" className="panel">
          <header>
            <h2>My skills</h2>
          </header>

          {/* New Skills Grid */}
          <section
            className="skills-section py-4"
            id="skills"
            aria-labelledby="skills-title"
          >
            <div className="container">
              {/* header intentionally minimal per request (no subtitle) */}

              <div className="row g-4">
                {/* Network Admin */}
                <div className="col-12 col-md-6 col-lg-4">
                  <article className="skill-card acc-cyan h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <img
                        className="skill-icon"
                        src="/assets/images/networking.png"
                        alt="Network Admin icon"
                      />
                      <h3 className="skill-title mb-0">Network Admin</h3>
                    </div>
                    <ul className="skill-list mb-0">
                      <li>VLANs, trunking, routing basics</li>
                      <li>Switch/router configuration & backups</li>
                      <li>Monitoring (SNMP, syslog, NetFlow)</li>
                      <li>Troubleshoot latency & packet loss</li>
                      <li>Document network topologies</li>
                    </ul>
                  </article>
                </div>

                {/* System Admin */}
                <div className="col-12 col-md-6 col-lg-4">
                  <article className="skill-card acc-indigo h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <img
                        className="skill-icon"
                        src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/hdd-stack.svg"
                        alt="System Admin icon"
                      />
                      <h3 className="skill-title mb-0">System Admin</h3>
                    </div>
                    <ul className="skill-list mb-0">
                      <li>Windows & Linux server provisioning</li>
                      <li>User/group management & IAM</li>
                      <li>Backup, restore, and patching</li>
                      <li>AD/DNS/DHCP configuration</li>
                      <li>SLA and uptime monitoring</li>
                    </ul>
                  </article>
                </div>

                {/* Linux Admin */}
                <div className="col-12 col-md-6 col-lg-4">
                  <article className="skill-card acc-orange h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <img
                        className="skill-icon"
                        src="/assets/images/Linux.png"
                        alt="Linux Admin icon"
                      />
                      <h3 className="skill-title mb-0">Linux Admin</h3>
                    </div>
                    <ul className="skill-list mb-0">
                      <li>Shell scripting & automation</li>
                      <li>Systemd services & log analysis</li>
                      <li>Package management (apt/yum/dnf)</li>
                      <li>Firewall (ufw, iptables) & hardening</li>
                      <li>Filesystem and permissions management</li>
                    </ul>
                  </article>
                </div>

                {/* Web Dev */}
                <div className="col-12 col-md-6 col-lg-4">
                  <article className="skill-card acc-purple h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <img
                        className="skill-icon"
                        src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/code-slash.svg"
                        alt="Web Dev icon"
                      />
                      <h3 className="skill-title mb-0">Web Dev</h3>
                    </div>
                    <ul className="skill-list mb-0">
                      <li>Responsive UI with HTML, CSS, Bootstrap</li>
                      <li>JavaScript interactivity & forms</li>
                      <li>Flask routing & Jinja templates</li>
                      <li>REST API integration & JSON handling</li>
                      <li>Linux deployment (Gunicorn/Nginx)</li>
                    </ul>
                  </article>
                </div>

                {/* Python */}
                <div className="col-12 col-md-6 col-lg-4">
                  <article className="skill-card acc-yellow h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <img
                        className="skill-icon"
                        src="/assets/images/Python.svg"
                        alt="Python icon"
                      />
                      <h3 className="skill-title mb-0">Python</h3>
                    </div>
                    <ul className="skill-list mb-0">
                      <li>Automation scripts & CLI tools</li>
                      <li>Data parsing (CSV, JSON)</li>
                      <li>API requests with requests</li>
                      <li>Virtualenv or Poetry management</li>
                      <li>Testing with pytest</li>
                    </ul>
                  </article>
                </div>

                {/* Cybersecurity */}
                <div className="col-12 col-md-6 col-lg-4">
                  <article className="skill-card acc-teal h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <img
                        className="skill-icon"
                        src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/shield-lock.svg"
                        alt="Cybersecurity icon"
                      />
                      <h3 className="skill-title mb-0">Cybersecurity</h3>
                    </div>
                    <ul className="skill-list mb-0">
                      <li>Principle of least privilege</li>
                      <li>Patch & vulnerability management</li>
                      <li>Secure configuration & secrets handling</li>
                      <li>Network segmentation & firewalls</li>
                      <li>Log review & incident response basics</li>
                    </ul>
                  </article>
                </div>
              </div>
            </div>
          </section>

          {/* Legacy section hidden by skills.css to keep markup light */}
          <section className="skill_class">
            <div id="languages">
              <div className="container">
                <div className="row">
                  <h1 className="section__title">
                    <strong className="text--purple other-font">
                      Web Development skills
                    </strong>
                  </h1>
                  <div className="language__list">
                    <div className="language">
                      <figure className="language__img--wrapper">
                        <img
                          src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/HTML5_Badge.svg/240px-HTML5_Badge.svg.png"
                          alt="Html Logo"
                          className="language__img"
                        />
                      </figure>
                      <span className="language__name">HTML</span>
                    </div>

                    <div className="language">
                      <figure className="language__img--wrapper">
                        <img
                          src="https://cdn.iconscout.com/icon/free/png-256/css-131-722685.png"
                          alt="CSS Logo"
                          className="language__img"
                        />
                      </figure>
                      <span className="language__name">CSS</span>
                    </div>

                    <div className="language">
                      <figure className="language__img--wrapper">
                        <img
                          src="https://cdn.iconscout.com/icon/free/png-256/javascript-1-225993.png"
                          alt="JavaScript Logo"
                          className="language__img"
                        />
                      </figure>
                      <span className="language__name">JavaScript</span>
                    </div>

                    <div className="language">
                      <figure className="language__img--wrapper">
                        <img
                          src="/assets/images/git.png"
                          alt="TypeScript Logo"
                          className="language__img"
                        />
                      </figure>
                      <span className="language__name">Git</span>
                    </div>

                    <div className="language">
                      <figure className="language__img--wrapper">
                        <img
                          src="/assets/images/php.png"
                          alt="React Logo"
                          className="language__img"
                        />
                      </figure>
                      <span className="language__name">PHP</span>
                    </div>

                    <div className="language">
                      <figure className="language__img--wrapper">
                        <img
                          src="/assets/images/Python.svg"
                          alt="React Logo"
                          className="language__img"
                        />
                      </figure>

                      <span className="language__name">Python</span>
                    </div>
                  </div>
                </div>
              </div>

              <hr className="the_hr" />

              <div className="container container-2">
                <div className="row">
                  <h1 className="section__title">
                    <strong className="text--blue other-font">
                      Computer Sciences skills
                    </strong>
                  </h1>

                  <div className="language__list">
                    <div className="skills">
                      <div className="child--help">
                        <div className="child">
                          <div className="click">
                            👋 Click here <span className="wave">👋</span>
                          </div>

                          <figure className="language__img--wrapper">
                            <img
                              src="/assets/images/networking.png"
                              alt="Html Logo"
                              className="language__img"
                            />
                          </figure>
                        </div>

                        <div className="child--description">
                          <h3>Computer Networking</h3>

                          <div className="descrip">
                            <ul>
                              <li>Networking device and cabling</li>

                              <hr />

                              <li>Network planning & designing process</li>

                              <hr />

                              <li>IP addressing & subnetting</li>

                              <hr />

                              <li>Cisco router & and Switch configuration</li>

                              <hr />

                              <li>OSI & TCP/IP</li>

                              <hr />

                              <li>Wireless networking</li>
                            </ul>
                          </div>
                        </div>
                      </div>

                      <div className="child--help">
                        <div className="child">
                          <div className="click">
                            👋 Click here <span className="wave">👋</span>
                          </div>

                          <figure className="language__img--wrapper">
                            <img
                              src="/assets/images/Linux.png"
                              alt="CSS Logo"
                              className="language__img"
                            />
                          </figure>
                        </div>

                        <div className="child--description">
                          <h3>Linux</h3>

                          <div className="descrip">
                            <ul>
                              <li>System Access and File System</li>

                              <hr />

                              <li>System Administration</li>

                              <hr />

                              <li>Shell Scripting</li>

                              <hr />

                              <li>Networking, Servers and System Updates</li>

                              <hr />

                              <li>Disk Management and Run Levels</li>
                            </ul>
                          </div>
                        </div>
                      </div>

                      <div className="child--help">
                        <div className="child">
                          <div className="click">
                            👋 Click here <span className="wave">👋</span>
                          </div>

                          <figure className="language__img--wrapper">
                            <img
                              src="/assets/images/Network_admin.png"
                              alt="JavaScript Logo"
                              className="language__img"
                            />
                          </figure>
                        </div>

                        <div className="child--description">
                          <h3>Network Admin</h3>

                          <div className="descrip">
                            <ul>
                              <li>Windows Server Administration</li>

                              <hr />

                              <li>Active Directory Domain Services</li>

                              <hr />

                              <li>Implementing and managing DHCP and DNS</li>

                              <hr />

                              <li>Managing file Servers and Storage</li>

                              <hr />

                              <li>Implementing VPN</li>

                              <hr />

                              <li>Performance Monitoring</li>
                            </ul>
                          </div>
                        </div>
                      </div>

                      <div className="child--help">
                        <div className="child">
                          <div className="click">
                            👋 Click here <span className="wave">👋</span>
                          </div>

                          <figure className="language__img--wrapper">
                            <img
                              src="/assets/images/telecom.png"
                              alt="JavaScript Logo"
                              className="language__img"
                            />
                          </figure>
                        </div>

                        <div className="child--description">
                          <h3>Telecommunication</h3>

                          <br />

                          <div className="descrip">
                            NOC Engineer <br />&<br /> Radio Frequency Design
                            Engineer <br />
                            <br />
                            <span> LinkedIn profile for more info -&gt;</span>
                            <a
                              href="https://www.linkedin.com/in/ma%C3%ABl-ma%C3%AEtre-9318a983/"
                              target="_blank"
                              className="about-me__link"
                            >
                              <i className="fab fa-brands fa-linkedin-in"></i>
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </article>

        {/* Tools */}
        <article id="tools" className="panel">
          <header>
            <h2>Project and Tools</h2>
          </header>

          <section className="tool-list">
            <h5 style={{ color: "red" }}>No tools for now</h5>
          </section>
        </article>

        {/* Contact me */}
        <article id="contact" className="panel">
          <header>
            <h2>Contact me</h2>
          </header>

          <section>
            <div className="row row-cols-1 row-cols-sm-2 g-4">
              <div className="col d-flex flex-column gap-2">
                <div className="feature-icon-small d-inline-flex align-items-center justify-content-center bg-gradient fs-4 rounded-3">
                  <a href="https://twitter.com/maelmaitre/" target="_blank">
                    <img
                      src="/assets/images/twitter.png"
                      alt=""
                      className="img_contact"
                    />
                  </a>
                </div>
                <a href="https://twitter.com/maelmaitre/" target="_blank">
                  <h4 className="fw-semibold mb-0 text-body-emphasis">
                    Twitter
                  </h4>
                </a>
              </div>

              <div className="col d-flex flex-column gap-2">
                <div className="feature-icon-small d-inline-flex align-items-center justify-content-center bg-gradient fs-4 rounded-3">
                  <a
                    href="https://www.linkedin.com/in/ma%C3%ABl-ma%C3%AEtre-9318a983//"
                    target="_blank"
                  >
                    <img
                      src="/assets/images/linkedin.svg"
                      alt=""
                      className="img_contact"
                    />
                  </a>
                </div>
                <a href="https://twitter.com/maelmaitre/" target="_blank">
                  <h4 className="fw-semibold mb-0 text-body-emphasis">
                    LinkedIn
                  </h4>
                </a>
              </div>

              <div className="col d-flex flex-column gap-2">
                <div className="feature-icon-small d-inline-flex align-items-center justify-content-center bg-gradient fs-4 rounded-3">
                  <a href="https://www.facebook.com/hackerhaiti/" target="_blank">
                    <img
                      src="/assets/images/facebook.png"
                      alt=""
                      className="img_contact"
                    />
                  </a>
                </div>
                <a href="https://twitter.com/maelmaitre/" target="_blank">
                  <h4 className="fw-semibold mb-0 text-body-emphasis">
                    Facebook
                  </h4>
                </a>
              </div>

              <div className="col d-flex flex-column gap-2">
                <div className="feature-icon-small d-inline-flex align-items-center justify-content-center bg-gradient fs-4 rounded-3">
                  <a href="https://twitter.com/maelmaitre/" target="_blank">
                    <img
                      src="/assets/images/instagram.jpg"
                      alt=""
                      className="img_contact"
                    />
                  </a>
                </div>
                <a href="https://www.instagram.com/maymaitre/" target="_blank">
                  <h4 className="fw-semibold mb-0 text-body-emphasis">
                    Instagram
                  </h4>
                </a>
              </div>
            </div>
          </section>
        </article>
      </div>

      {/* Footer */}
      <div id="footer">
        <ul className="copyright">
          {/* <li>Design: Maël Maître & <a href="http://html5up.net" target="_blank">HTML5 UP</a></li>*/}
        </ul>
      </div>
    </div>
  );
}
