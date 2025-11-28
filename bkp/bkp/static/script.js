// static/script.js
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const inputText = document.getElementById('inputText');
const resultBox = document.getElementById('result');
const resultBadge = document.getElementById('resultBadge');
const resultLabel = document.getElementById('resultLabel');
const resultConf = document.getElementById('resultConf');

analyzeBtn.addEventListener('click', () => doAnalyze());
clearBtn.addEventListener('click', () => {
  inputText.value = '';
  hideResult();
});

async function doAnalyze(){
  const text = inputText.value.trim();
  if(!text){
    alert('Cole o texto da notícia antes de analisar.');
    return;
  }

  showLoading();

  try {
    const resp = await fetch('/analisar', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({texto: text})
    });
    const data = await resp.json();
    if(resp.ok){
      showResult(data);
    } else {
      alert(data.error || 'Erro na análise.');
      hideResult();
    }
  } catch (err) {
    console.error(err);
    alert('Erro ao conectar com o servidor. Verifique se o backend está rodando.');
    hideResult();
  }
}

function showLoading(){
  resultBox.classList.remove('hidden');
  resultBadge.textContent = '...';
  resultBadge.classList.remove('fake','real');
  resultLabel.textContent = 'Analisando...';
  resultConf.textContent = '';
}

function showResult(data){
  if(data.resultado === 'FAKE'){
    resultBadge.textContent = 'FAKE';
    resultBadge.classList.remove('real');
    resultBadge.classList.add('fake');
    resultLabel.textContent = 'Resultado: FAKE';
  } else {
    resultBadge.textContent = 'VERDADEIRA';
    resultBadge.classList.remove('fake');
    resultBadge.classList.add('real');
    resultLabel.textContent = 'Resultado: VERDADEIRA';
  }
  if(data.prob_fake !== null && data.prob_fake !== undefined){
    const conf = (data.prob_fake*100).toFixed(1) + '% (prob fake)';
    resultConf.textContent = conf;
  } else {
    resultConf.textContent = 'Confiança: N/A';
  }
}

function hideResult(){
  resultBox.classList.add('hidden');
  resultBadge.textContent = '—';
  resultBadge.classList.remove('fake','real');
  resultLabel.textContent = 'Resultado';
  resultConf.textContent = 'Confiança: —';
}
