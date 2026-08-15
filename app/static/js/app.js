document.addEventListener('DOMContentLoaded', function () {
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  const token = localStorage.getItem('accessToken') || getCookie('access_token');
  let user = {};

  try {
    const storedUser = localStorage.getItem('user');
    user = storedUser ? JSON.parse(storedUser) : {};
  } catch (error) {
    user = {};
  }

  const logoutBtn = document.getElementById('logoutBtn');
  const userNavBadge = document.getElementById('userNavBadge');
  const publicLinks = document.querySelectorAll('.public-link');
  const authLinks = document.querySelectorAll('.auth-link');
  const cLevelLinks = document.querySelectorAll('.c-level-link');

  function updateAuthUI() {
    const hasToken = Boolean(token);
    const isCLevel = userHasRole('c-level');

    if (logoutBtn) {
      logoutBtn.classList.toggle('d-none', !hasToken);
    }

    publicLinks.forEach(link => {
      link.classList.toggle('d-none', hasToken);
    });

    authLinks.forEach(link => {
      link.classList.toggle('d-none', !hasToken);
    });

    cLevelLinks.forEach(link => {
      link.classList.toggle('d-none', !(hasToken && isCLevel));
    });

    if (userNavBadge) {
      if (hasToken && user.user_id) {
        const roleText = (user.user_role || []).join(', ') || 'No role';
        userNavBadge.textContent = `${user.user_id} • ${roleText}`;
        userNavBadge.classList.remove('d-none');
      } else {
        userNavBadge.textContent = '';
        userNavBadge.classList.add('d-none');
      }
    }
  }

  function userHasRole(role) {
    const roles = (user.user_role || []).map(r => String(r).toLowerCase());
    return roles.includes(String(role).toLowerCase());
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', function () {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('conversationId');
      localStorage.removeItem('user');
      localStorage.removeItem('chatHistory');
      document.cookie = 'access_token=; Max-Age=0; path=/';
      document.cookie = 'refresh_token=; Max-Age=0; path=/';
      document.cookie = 'conversation_id=; Max-Age=0; path=/';
      window.location.href = '/login';
    });
  }

  updateAuthUI();

  if (['/chat', '/admin', '/dashboard', '/upload'].includes(window.location.pathname) && !token) {
    window.location.href = '/login';
  }

  if (window.location.pathname === '/admin' && token && !userHasRole('c-level')) {
    window.location.href = '/chat';
  }

  if (window.location.pathname === '/dashboard' && token && !userHasRole('c-level')) {
    window.location.href = '/chat';
  }

  if (window.location.pathname === '/upload' && token && !userHasRole('c-level')) {
    window.location.href = '/chat';
  }

  const userBadge = document.getElementById('userBadge');
  if (window.location.pathname !== '/login' && user.user_id && userBadge) {
    const userRole = (user.user_role || []).join(', ');
    userBadge.textContent = (user.user_id || 'User') + ' • ' + userRole;
  }
});
