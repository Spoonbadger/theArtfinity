const hideAlerts = (hideDelay = 3000, alertSelector=".alert.alert-dismissible") => {
  const alerts = document.querySelectorAll(alertSelector);

  alerts.forEach(alert => {
    setTimeout(() => { alert.classList.add('fade') }, hideDelay);
  });
}

const init = () => {
  // Hide All alerts after few seconds 
  hideAlerts();
};

// Runs when DOM is loaded successfully
document.addEventListener('DOMContentLoaded', init, false);