// Método rápido para avaliar todas as disciplinas

// Após abrir a pagina de avaliação do docente, digite ctrl + shift + i para abrir o console do navegador
// Seu console pode esta bloqueado para colar scripts, entao digite permitir colar e aperte enter
// Agora cole o código abaixo e pressione enter


const selects = document.querySelectorAll('select[name^="p_"]');

selects.forEach(select => {
    select.value = "5";
});
