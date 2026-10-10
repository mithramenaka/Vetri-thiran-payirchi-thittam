const taskSelect =
    document.getElementById("task");

const input =
    document.getElementById("user-input");

const levelContainer =
    document.getElementById("level-container");

const levelSelect =
    document.getElementById("level");

const submitButton =
    document.getElementById("submit-button");

const buttonText =
    document.getElementById("button-text");

const loadingSpinner =
    document.getElementById("loading-spinner");

const resultCard =
    document.getElementById("result-card");

const resultContent =
    document.getElementById("result-content");

const errorMessage =
    document.getElementById("error-message");

const copyButton =
    document.getElementById("copy-button");

const characterCount =
    document.getElementById("character-count");


/* -----------------------------
   TASK UI
----------------------------- */

taskSelect.addEventListener(
    "change",
    updateTaskUI
);


function updateTaskUI() {

    const task =
        taskSelect.value;


    if (task === "learn") {

        levelContainer.classList.remove(
            "hidden"
        );

        input.placeholder =
            "Example: Learn Python programming";

    } else {

        levelContainer.classList.add(
            "hidden"
        );


        if (task === "qa") {

            input.placeholder =
                "Example: What is photosynthesis?";

        } else if (task === "explain") {

            input.placeholder =
                "Example: Explain the Pythagoras theorem.";

        } else if (task === "quiz") {

            input.placeholder =
                "Paste your study material here.";

        } else if (task === "summarize") {

            input.placeholder =
                "Paste the paragraph or study material here.";

        }

    }


    updateButtonText();
}


/* -----------------------------
   BUTTON TEXT
----------------------------- */

function updateButtonText() {

    const labels = {

        qa:
            "Get Answer",

        explain:
            "Explain Topic",

        quiz:
            "Generate Quiz",

        summarize:
            "Summarize Text",

        learn:
            "Create Learning Path"

    };


    buttonText.textContent =
        labels[taskSelect.value];
}


/* -----------------------------
   CHARACTER COUNTER
----------------------------- */

input.addEventListener(
    "input",
    function () {

        characterCount.textContent =
            input.value.length;

    }
);


/* -----------------------------
   SUBMIT
----------------------------- */

submitButton.addEventListener(
    "click",
    submitRequest
);


async function submitRequest() {

    clearError();


    const task =
        taskSelect.value;

    const text =
        input.value.trim();


    if (!text) {

        showError(
            "Please enter some content first."
        );

        return;
    }


    if (text.length > 20000) {

        showError(
            "Your input is too long."
        );

        return;
    }


    setLoading(true);


    try {

        const request =
            buildRequest(
                task,
                text
            );


        const response =
            await fetch(
                request.url,
                {
                    method:
                        "POST",

                    headers:
                        {
                            "Content-Type":
                                "application/json"
                        },

                    body:
                        JSON.stringify(
                            request.body
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "EduGenie could not process your request."
            );

        }


        showResult(
            task,
            data
        );


    } catch (error) {

        showError(
            error.message
        );


    } finally {

        setLoading(false);

    }

}


/* -----------------------------
   BUILD REQUEST
----------------------------- */

function buildRequest(
    task,
    text
) {

    if (task === "qa") {

        return {

            url:
                "/qa",

            body:
                {
                    question:
                        text
                }

        };

    }


    if (task === "explain") {

        return {

            url:
                "/explain",

            body:
                {
                    text:
                        text
                }

        };

    }


    if (task === "quiz") {

        return {

            url:
                "/quiz",

            body:
                {
                    text:
                        text
                }

        };

    }


    if (task === "summarize") {

        return {

            url:
                "/summarize",

            body:
                {
                    text:
                        text
                }

        };

    }


    if (task === "learn") {

        return {

            url:
                "/learn/recommendations",

            body:
                {
                    topic:
                        text,

                    level:
                        levelSelect.value
                }

        };

    }


    throw new Error(
        "Invalid task selected."
    );
}


/* -----------------------------
   SHOW RESULT
----------------------------- */

function showResult(
    task,
    data
) {

    resultCard.classList.remove(
        "hidden"
    );


    if (task === "quiz") {

        renderQuiz(
            data.questions
        );

    } else {

        resultContent.textContent =
            data.result ||
            "No result was returned.";

    }


    resultCard.scrollIntoView(
        {
            behavior:
                "smooth",

            block:
                "start"
        }
    );
}


/* -----------------------------
   QUIZ
----------------------------- */

function renderQuiz(
    questions
) {

    resultContent.innerHTML = "";


    if (
        !Array.isArray(questions)
        ||
        questions.length === 0
    ) {

        resultContent.textContent =
            "No questions were generated.";

        return;
    }


    questions.forEach(
        function (
            question,
            index
        ) {

            const container =
                document.createElement(
                    "div"
                );

            container.className =
                "quiz-question";


            const heading =
                document.createElement(
                    "h3"
                );

            heading.textContent =
                `${index + 1}. ${question.question}`;


            container.appendChild(
                heading
            );


            question.options.forEach(
                function (option) {

                    const button =
                        document.createElement(
                            "button"
                        );

                    button.className =
                        "quiz-option";

                    button.textContent =
                        option;


                    button.addEventListener(
                        "click",
                        function () {

                            checkAnswer(
                                button,
                                option,
                                question.correct_answer,
                                question.explanation,
                                container
                            );

                        }
                    );


                    container.appendChild(
                        button
                    );

                }
            );


            resultContent.appendChild(
                container
            );

        }
    );
}


/* -----------------------------
   CHECK ANSWER
----------------------------- */

function checkAnswer(
    selectedButton,
    selectedAnswer,
    correctAnswer,
    explanation,
    container
) {

    const buttons =
        container.querySelectorAll(
            ".quiz-option"
        );


    buttons.forEach(
        function (button) {

            button.disabled =
                true;


            if (
                button.textContent ===
                correctAnswer
            ) {

                button.classList.add(
                    "correct"
                );

            }

        }
    );


    if (
        selectedAnswer !==
        correctAnswer
    ) {

        selectedButton.classList.add(
            "wrong"
        );

    }


    const explanationElement =
        document.createElement(
            "div"
        );

    explanationElement.className =
        "quiz-explanation";


    if (
        selectedAnswer ===
        correctAnswer
    ) {

        explanationElement.textContent =
            "Correct! " +
            explanation;

    } else {

        explanationElement.textContent =
            `Incorrect. Correct answer: ${correctAnswer}. ${explanation}`;

    }


    container.appendChild(
        explanationElement
    );
}


/* -----------------------------
   COPY
----------------------------- */

copyButton.addEventListener(
    "click",
    async function () {

        try {

            await navigator.clipboard.writeText(
                resultContent.innerText
            );


            const oldText =
                copyButton.textContent;


            copyButton.textContent =
                "Copied!";


            setTimeout(
                function () {

                    copyButton.textContent =
                        oldText;

                },
                1500
            );


        } catch {

            showError(
                "Could not copy the result."
            );

        }

    }
);


/* -----------------------------
   LOADING
----------------------------- */

function setLoading(
    loading
) {

    submitButton.disabled =
        loading;


    if (loading) {

        loadingSpinner.classList.remove(
            "hidden"
        );

        buttonText.textContent =
            "EduGenie is thinking...";

    } else {

        loadingSpinner.classList.add(
            "hidden"
        );

        updateButtonText();

    }
}


/* -----------------------------
   ERROR
----------------------------- */

function showError(
    message
) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );
}


function clearError() {

    errorMessage.textContent =
        "";

    errorMessage.classList.add(
        "hidden"
    );
}


/* -----------------------------
   INITIALIZE
----------------------------- */

updateTaskUI();