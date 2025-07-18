const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');
const menuIcon = document.querySelector('.menu-icon');
const dropdownMenu = document.getElementById("dropdownMenu");

// Ensure elements exist before adding event listeners
if (registerLink && loginLink && wrapper) {
    registerLink.addEventListener('click', () => {
        wrapper.classList.add('active');
    });

    loginLink.addEventListener('click', () => {
        wrapper.classList.remove('active');
    });
}

if (btnPopup && wrapper) {
    btnPopup.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
    });
}

if (iconClose && wrapper) {
    iconClose.addEventListener('click', () => {
        wrapper.classList.remove('active-popup');
    });
}

// Toggle Main Menu (Hamburger Menu)
if (menuIcon && dropdownMenu) {
    menuIcon.addEventListener("click", () => {
        dropdownMenu.classList.toggle("active");
    });

    // Close menu when clicking outside
    document.addEventListener("click", (event) => {
        if (!menuIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove("active");
        }
    });
}

// Toggle Submenus for Departments, Alumni, and Committees
function toggleSubMenu(id) {
    const submenu = document.getElementById(id);
    if (submenu) {
        // Close all other open submenus before opening the clicked one
        document.querySelectorAll(".submenu").forEach(menu => {
            if (menu !== submenu) {
                menu.classList.remove("active");
            }
        });

        submenu.classList.toggle("active");
    }
}
