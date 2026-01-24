document.addEventListener("DOMContentLoaded", () => {
    console.log("Home.js loaded!");

    /* ================= SCROLL ANIMATION ================= */
    const scrollElements = document.querySelectorAll(".scroll-element");

    const elementInView = (el, dividend = 1.25) => {
        const elementTop = el.getBoundingClientRect().top;
        return elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend;
    };

    const handleScrollAnimation = () => {
        scrollElements.forEach(el => {
            el.classList.toggle("scrolled", elementInView(el));
        });
    };

    window.addEventListener("scroll", handleScrollAnimation);

    /* ================= HERO SLIDER ================= */
    const heroSection = document.querySelector(".hero-section");
    if (heroSection) {
        const slides = heroSection.querySelectorAll(".hero-slide");
        let index = 0;

        if (slides.length) {
            slides[index].classList.add("active");
            setInterval(() => {
                slides[index].classList.remove("active");
                index = (index + 1) % slides.length;
                slides[index].classList.add("active");
            }, 4000);
        }
    }

    /* ================= LIVE SEARCH ================= */
    const searchInput = document.getElementById("live-search-input");
    const resultsDiv = document.getElementById("live-search-results");
    const productCards = document.querySelectorAll(".product-card");

    if (searchInput && resultsDiv) {
        searchInput.addEventListener("input", () => {
            const filter = searchInput.value.toLowerCase().trim();
            resultsDiv.innerHTML = "";

            if (!filter) {
                resultsDiv.style.display = "none";
                return;
            }

            let hasResults = false;

            productCards.forEach(card => {
                const link = card.querySelector("h3 a");
                if (!link) return;

                if (link.textContent.toLowerCase().includes(filter)) {
                    hasResults = true;
                    resultsDiv.innerHTML += `
                        <div class="search-item" data-url="${link.href}">
                            ${link.textContent}
                        </div>
                    `;
                }
            });

            resultsDiv.style.display = hasResults ? "block" : "none";
        });

        resultsDiv.addEventListener("click", e => {
            if (e.target.classList.contains("search-item")) {
                window.location.href = e.target.dataset.url;
            }
        });

        document.addEventListener("click", e => {
            if (!searchInput.contains(e.target) && !resultsDiv.contains(e.target)) {
                resultsDiv.style.display = "none";
            }
        });
    }

    /* ================= SCROLL TO TOP ================= */
    const scrollTopBtn = document.getElementById("scrollTop");
    if (scrollTopBtn) {
        window.addEventListener("scroll", () => {
            scrollTopBtn.classList.toggle("show", window.scrollY > 300);
        });

        scrollTopBtn.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    /* ================= BUTTON HOVER ================= */
    document.querySelectorAll(".btn-hover").forEach(btn => {
        btn.addEventListener("mouseenter", () => btn.classList.add("hovered"));
        btn.addEventListener("mouseleave", () => btn.classList.remove("hovered"));
    });
});