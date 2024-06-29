
correct_btn = document.getElementById('correct_btn');
wrong_btn = document.getElementById('wrong_btn');
question = document.getElementById('question');
answer = document.getElementById('answer');
flip_card = document.querySelector('.flip-card');
flip_card_inner = document.querySelector('.flip-card-inner');
add_card = document.getElementById('add_card');
card_form = document.querySelector('.card_form');
flashcard = document.querySelector('.flashcard');
memory_score = document.getElementById('memory_score');
buttons = document.querySelector('.buttons');
try_again = document.querySelector('.try_again');

let wrong_count = 0;
let correct_count = 0;

let close_btn = `
    <button  class="btn">
    <a href="/main_page" class="ps-1"><img src="/static/images/exit2.png" 
    alt="home" style="width: 40px; height: 40px;" data-toggle="tooltip" title="Exit"></a>
    </button>
`
let repeat_btn = `
    <button  class="btn try_again">
    <a href="" class="pe-1"><img src="/static/images/repeat2.png" 
    alt="home" style="width: 40px; height: 40px;" data-toggle="tooltip" title="Try again"></a>
    </button>
`;

if (add_card){
    add_card.addEventListener('click', function() {
        console.log('add card clicked');
        let question_answer = `
            <div class="d-flex justify-content-between">
                <div class="mb-2 w-50 p-4">
                    <label for="question" class="form-label">Question</label>
                    <input type="text" class="form-control" id="question" name="question">
                </div>
                <div class="mb-2 w-50 p-4">
                    <label for="answer" class="form-label">Answer</label>
                    <input type="text" class="form-control" id="answer" name="answer">
                </div>
            </div>
        `;
    
        card_form.insertAdjacentHTML('beforebegin', question_answer);
    });
}



let currentIndex = 0;
question.innerText = flashcardData[currentIndex] ? flashcardData[currentIndex].question : '';
answer.innerText = flashcardData[currentIndex] ? flashcardData[currentIndex].answer : '';

function flipCard() {
    document.querySelector('.flip-card-inner').classList.toggle('rotate');
}

flip_card_inner.addEventListener('click', flipCard);

function redirectToPage(url) {
    window.location.href = url;
}

handle_wrong_check_button =  () => {
    console.log('flashcardLength:', flashcardData.length)
    console.log('currentIndex:', currentIndex)
    if (currentIndex < flashcardData.length-1) {
        
        flip_card_inner.classList.remove('rotate');
        flip_card.classList.remove('animate__slideInLeft');
        flip_card.classList.add('animate__fadeOutRight');
        currentIndex++;
        console.log('currentIndex:', currentIndex )
        setTimeout(() => {
            question.innerText = flashcardData[currentIndex].question;
            answer.innerText = flashcardData[currentIndex].answer;
            
        }, 1000);
        
        setTimeout(() => {
            flip_card.classList.remove('animate__fadeOutRight');
            flip_card.classList.add('animate__slideInLeft');
        }, 1000);
    }else {
        flip_card_inner.removeEventListener('click', flipCard);  
        // console.log('correct_count:', correct_count)
        // console.log('wrong_count:', wrong_count)
        // console.log('flashcardData.length:', flashcardData.length)
        question.innerText = 'Memory Score: ' + ((correct_count/flashcardData.length)*100).toFixed(0) + '%';
        if (correct_btn){
            correct_btn.remove();
        }
        if (wrong_btn){
            wrong_btn.remove();
        }

        buttons.insertAdjacentHTML('afterbegin', repeat_btn); //afterbegin - Insert a new div as the first child
        buttons.insertAdjacentHTML('beforeend', close_btn); // beforeend - Insert a new div as the last child

    }
}

if (correct_btn){
    correct_btn.addEventListener('click', function() {
        correct_count++;
        handle_wrong_check_button();
        
    });
}

if (wrong_btn){
    wrong_btn.addEventListener('click', function() {
        wrong_count++;
        handle_wrong_check_button();
        
    });
}


try_again.addEventListener('click', function() {
    window.location.reload();
});