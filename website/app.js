/**
 * BIOPITCH LAB & MEDICAL CARE PLATFORM - CLIENT SCRIPT
 * B2C 선수 1:1 예약 모달, B2B 아카데미 제휴 신청 폼, 모바일 드로어 및 토스트 알림
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Mobile Drawer Navigation
  const mobileMenuBtn = document.getElementById("mobileMenuBtn");
  const mobileDrawer = document.getElementById("mobileDrawer");
  const drawerCloseBtn = document.getElementById("drawerCloseBtn");
  const mobileLinks = document.querySelectorAll(".mobile-link");

  const openDrawer = () => {
    mobileDrawer.classList.add("active");
    document.body.style.overflow = "hidden";
  };

  const closeDrawer = () => {
    mobileDrawer.classList.remove("active");
    document.body.style.overflow = "";
  };

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener("click", openDrawer);
  }

  if (drawerCloseBtn && mobileDrawer) {
    drawerCloseBtn.addEventListener("click", closeDrawer);
  }

  mobileLinks.forEach((link) => {
    link.addEventListener("click", closeDrawer);
  });

  // 2. B2C Booking Modal Logic
  const bookingModal = document.getElementById("bookingModal");
  const modalCloseBtn = document.getElementById("modalCloseBtn");
  const openBookingBtns = document.querySelectorAll(".open-booking-btn");
  const selectCenter = document.getElementById("selectCenter");
  const b2cBookingForm = document.getElementById("b2cBookingForm");

  const openModal = (centerName = null) => {
    if (bookingModal) {
      bookingModal.classList.add("active");
      document.body.style.overflow = "hidden";
      if (centerName && selectCenter) {
        selectCenter.value = centerName;
      }
    }
  };

  const closeModal = () => {
    if (bookingModal) {
      bookingModal.classList.remove("active");
      document.body.style.overflow = "";
    }
  };

  openBookingBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      closeDrawer();
      const centerName = btn.getAttribute("data-center");
      openModal(centerName);
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener("click", closeModal);
  }

  if (bookingModal) {
    bookingModal.addEventListener("click", (e) => {
      if (e.target === bookingModal) {
        closeModal();
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && bookingModal && bookingModal.classList.contains("active")) {
      closeModal();
    }
  });

  // 3. Toast Notification Helper
  const toast = document.getElementById("toastNotification");
  const toastMessage = document.getElementById("toastMessage");
  let toastTimer = null;

  const showToast = (message, isSuccess = true) => {
    if (!toast || !toastMessage) return;

    clearTimeout(toastTimer);
    toastMessage.textContent = message;
    toast.classList.add("active");

    toastTimer = setTimeout(() => {
      toast.classList.remove("active");
    }, 4000);
  };

  // 4. B2C Booking Form Submission Handler
  if (b2cBookingForm) {
    b2cBookingForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const playerName = document.getElementById("playerName").value.trim();
      const playerPhone = document.getElementById("playerPhone").value.trim();
      const center = selectCenter.value;

      const submitBtn = document.getElementById("bookingSubmitBtn");
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> 접수 처리 중...`;

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa-solid fa-check"></i> 1:1 케어 예약 신청 완료하기`;
        closeModal();
        b2cBookingForm.reset();

        showToast(`[${playerName} 선수] 1:1 케어 예약이 접수되었습니다! 담당 디렉터가 ${playerPhone}로 곧 확정 연락을 드립니다.`);
      }, 700);
    });
  }

  // 5. B2B Academy Partnership Form Handler
  const b2bForm = document.getElementById("b2bInquiryForm");
  if (b2bForm) {
    b2bForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const academyName = document.getElementById("academyName").value.trim();
      const ownerName = document.getElementById("ownerName").value.trim();
      const ownerPhone = document.getElementById("ownerPhone").value.trim();

      const submitBtn = document.getElementById("b2bSubmitBtn");
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> 제휴 신청서 접수 중...`;

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa-solid fa-paper-plane"></i> 메디컬 룸 도입 및 인력 매칭 제휴 신청하기`;
        b2bForm.reset();

        showToast(`[${academyName} / ${ownerName} 대표님] B2B 제휴 신청이 정상 완료되었습니다! 박인국 총괄 디렉터가 ${ownerPhone}로 실측 방문 일정을 조율해 드립니다.`);
      }, 800);
    });
  }

  // 6. Header Scrolled Styling
  const mainHeader = document.getElementById("mainHeader");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 40) {
      mainHeader.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.6)";
      mainHeader.style.borderBottomColor = "rgba(56, 189, 248, 0.2)";
    } else {
      mainHeader.style.boxShadow = "none";
      mainHeader.style.borderBottomColor = "var(--border-subtle)";
    }
  });
});
