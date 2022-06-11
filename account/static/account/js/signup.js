(() => {
  const jsAgreeRuleId = document.getElementById('js-agree-rule');
  if (jsAgreeRuleId) {
    const jsSignupButtonId = document.getElementById('js-signup-button');
    jsAgreeRuleId.addEventListener('click', (e) => {
      if (jsAgreeRuleId.checked) {
        jsSignupButtonId.classList.remove('opacity-50', 'cursor-not-allowed');
        jsSignupButtonId.disabled = false;
      } else {
        jsSignupButtonId.classList.add('opacity-50', 'cursor-not-allowed');
        jsSignupButtonId.disabled = true;
      }
    });
  }
})();