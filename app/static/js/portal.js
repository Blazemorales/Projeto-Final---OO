document.addEventListener("DOMContentLoaded", function() {
    const img_button = document.querySelector("img");

    if (img_button) {
        img_button.addEventListener("click", function() {
            showAnimatedMessage("Redirecionando para login...");
        });
    }

    function showAnimatedMessage(message) {
        //Mostra a mensagem
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('animated-message');
        messageDiv.innerText = message;
        document.body.appendChild(messageDiv);

        //Timer da mensagem
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 2000);
    }
});
