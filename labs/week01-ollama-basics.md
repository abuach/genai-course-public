# CS238
# Instructor: Chiké Abuah
# Week 1 Lab: The Prediction Machine

**Lab Duration:** ~50 minutes
**Reading:** Chapter 1 (Introduction) of *Illustrating Generative AI*

---

## Learning Objectives

By the end of this lab, you will be able to:
- Run a language model from Python with the book's `genai` library
- Tell a *discriminative* task (pick from existing options) from a *generative* one (make something new)
- Look inside the prediction machine: read a model's probabilities for the next token, and tell a *peaked* forecast from a *spread* one

---

## Prerequisites

- No prior coding or GenAI experience is required.
- Read Chapter 1. This lab reruns its experiments, so you'll recognize every one.
- If you can, do the **Setup** steps below before class.

---

## Setup

You'll keep all of this quarter's lab work in one folder on your laptop, managed by `uv`, a fast all-in-one tool for Python projects.

1. **Skip this step if you're on a campus computer; `uv` is already installed.** On your own laptop, install [uv](https://docs.astral.sh/uv/). On macOS or Linux:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   On Windows (PowerShell):
   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   Then close the terminal and open a new one so the `uv` command is found.
2. Install the Python version the course uses. `uv` downloads and manages it for you, separate from any other Python on your machine:
   ```bash
   uv python install 3.13
   ```
3. Make a folder for the course and turn it into a `uv` project that uses Python 3.13:
   ```bash
   mkdir cs238
   ```
   ```bash
   cd cs238
   ```
   ```bash
   uv init --python 3.13
   ```
4. Add the book's companion library, `genai`, to the project:
   ```bash
   uv add git+https://github.com/abuach/illustrating-genai-examples
   ```
5. Point `genai` at the class Ollama server, `ollama2.cs.wallawalla.edu`. The models all live there, so there's nothing big to download. You only do this once; it sets `OLLAMA_HOST`, the variable Ollama's tools (and `genai`) read to find their server.

   On a campus computer (Linux), add the setting to your shell's startup file, then load it into the terminal you have open:
   ```bash
   echo 'export OLLAMA_HOST=http://ollama2.cs.wallawalla.edu:11434' >> ~/.bashrc
   ```
   ```bash
   source ~/.bashrc
   ```
   Every new terminal you open from now on picks the setting up automatically.

   On your own laptop, use the command for your system instead, then **close the terminal, open a new one, and `cd` back into `cs238`**. On macOS:
   ```bash
   echo 'export OLLAMA_HOST=http://ollama2.cs.wallawalla.edu:11434' >> ~/.zshrc
   ```
   On Windows (PowerShell):
   ```bash
   setx OLLAMA_HOST "http://ollama2.cs.wallawalla.edu:11434"
   ```
6. Check which server `genai` will use:
   ```bash
   uv run python -c "from genai import get_host; print(get_host())"
   ```
   It should print `http://ollama2.cs.wallawalla.edu:11434`.

The class server is shared, so please follow the [server guidelines](https://github.com/abuach/genai-course-public/blob/main/resources/ollama-server-guidelines.md).

---

## How Every Lab Works

Every lab works from your `cs238` folder. Save each script in that week's folder, and run it with `uv run`:

```bash
mkdir -p labs/week01
```

```bash
uv run labs/week01/check_setup.py
```

When a script draws a chart, it opens in its own window and is also saved as a `.png` next to your script. **Close the chart window to let the script continue.**

Model output changes from run to run, so your answers won't match the book word for word. What should hold is the *shape* of each result.

### Working Off Campus

The class server may only be reachable from the campus network. Off campus, either connect to the university VPN, or run the models on your own laptop instead:

1. Install [Ollama](https://ollama.com) and open the app.
2. Point this terminal (just this one) back at your laptop. On macOS or Linux:
   ```bash
   export OLLAMA_HOST=http://localhost:11434
   ```
   On Windows (PowerShell):
   ```bash
   $env:OLLAMA_HOST = "http://localhost:11434"
   ```
3. Download the models the lab uses. Each lab lists them under **Working locally?** This week it's:
   ```bash
   ollama pull gemma4
   ```
   ```bash
   ollama pull llama3.2
   ```
   `gemma4` is about 10 GB and `llama3.2` about 2 GB, so do this on a fast connection.

Run the `ollama pull` commands *after* step 2. Otherwise `ollama` sends them to the class server instead of your laptop. A new terminal goes back to the class server automatically.

Alternatively, to switch servers inside a single script, put this at the top: `from genai import set_host` and then `set_host("http://localhost:11434")`.

---

## Part 0: Setup Check (6 minutes)

Create `labs/week01/check_setup.py`. It's the chapter's own setup check:

```python
from genai import ask

# If this returns a response, your setup is working!
print(ask("What does generative mean?"))
```

```bash
uv run labs/week01/check_setup.py
```

**Checkpoint:** You should see a short definition. If you get a connection error, check that you're on the campus network (or VPN) and that `get_host()` prints the class server. Working locally? Make sure the Ollama app is running.

**Task 0 (the chapter's Warm-Up):** Run the same script two more times. The wording drifts a little on each run. Chapter 2 explains exactly why; for now, just notice it.

---

## Part 1: The Jigsaw and the LEGO (7 minutes)

The chapter's picture: *discriminative* AI solves a jigsaw puzzle, placing a piece where it belongs among options that already exist, while *generative* AI plays with LEGO bricks and builds something new. A modern LLM can do both.

Create `labs/week01/jigsaw_and_lego.py`:

```python
from genai import ask

review = ("I felt like part one was more fast-paced and exciting, "
          "but the soundtrack in part two was more emotionally "
          "satisfying.")

# Discriminative: choose one of three labels that already exist
label = ask("Classify as POSITIVE, NEGATIVE, or MIXED. "
            f"One word.\n{review}")
print(f"Discriminate → {label}")

# Generative: make something that didn't exist before
new_review = ask("Write a one-sentence MIXED review of a movie sequel.")
print(f"Generate     → {new_review}")
```

```bash
uv run labs/week01/jigsaw_and_lego.py
```

**Task 1:** Change `review` to one you write yourself that should be hard to label, like a sarcastic one ("Oh great, *another* three-hour superhero movie."). Does the model get it right? Keep your review and its label for the lab questions.

---

## Part 2: Inside the Prediction Machine (14 minutes)

Before it writes each token, a language model scores every token it knows and turns those scores into probabilities. `next_token_distribution` asks Ollama for the top few, and `plot_next_token` draws them as the chapter's bar charts.

### 2.1 One Obvious Answer, One Long Shot

Create `labs/week01/predict.py`:

```python
from genai import ask, next_token_distribution
from genai.viz import plot_next_token, plot_two_step

MODEL = "llama3.2:latest"
prompt = "The capital of the USA is"

# 1. The model's forecast for the first word of its answer
dist = next_token_distribution(prompt, model=MODEL, top_k=6)
plot_next_token(prompt, dist, "labs/week01/washington.png")

# 2. Commit to the long shot: start the model's own answer with "New"
step2 = next_token_distribution(prompt, model=MODEL, top_k=6,
                                reply_start="New")
plot_two_step(prompt, "New", dist, step2, "labs/week01/new_york.png")

# 3. The same words, sent as a message of our own instead
print(ask("The capital of the USA is New", model=MODEL,
          options={"temperature": 0}))
```

```bash
uv run labs/week01/predict.py
```

Compare with the chapter. The first chart should be steeply *peaked* on "Washington." Once "New" is written into the model's *own* reply, it rushes on to "York." But send the same words as a *message* and it corrects you instead.

### 2.2 A Door That Opens Onto Anything

Now the chapter's open-ended story prompt, predicted two words in a row. Create `labs/week01/door.py`:

```python
from genai import next_token_distribution
from genai.viz import plot_two_step

MODEL = "llama3.2:latest"
door = "She opened the door and saw a"

# 1. The forecast for the first word: many reasonable options
step1 = next_token_distribution(door, model=MODEL, top_k=6)

# 2. Lock in the favorite and forecast the word after it
top_word = step1[0][0]
step2 = next_token_distribution(door, model=MODEL, top_k=6,
                                reply_start=top_word)
plot_two_step(door, top_word, step1, step2, "labs/week01/door.png")
```

```bash
uv run labs/week01/door.py
```

The first step should be *spread* across many reasonable words, and the second step should snap shut once the first word is locked in.

### 2.3 Your Turn: Predict, Then Peek

This is the chapter's Exercise 1. Write two unfinished sentences of your own:
- one where you expect the model to be **very sure** of the next word, and
- one where you expect **almost anything** could come next.

**Before running anything**, write down which one you expect to be peaked and what you think its top candidates will be. Then create `labs/week01/my_prompts.py` and replace the two example prompts with yours:

```python
from genai import next_token_distribution
from genai.viz import plot_next_token

MODEL = "llama3.2:latest"
sure = "Twinkle, twinkle, little"            # ← your "very sure" sentence
anything = "My favorite thing to eat is"     # ← your "almost anything" sentence

for name, prompt in [("sure", sure), ("anything", anything)]:
    dist = next_token_distribution(prompt, model=MODEL, top_k=6)
    plot_next_token(prompt, dist, f"labs/week01/{name}.png")
```

```bash
uv run labs/week01/my_prompts.py
```

**Task 2:** Were your predictions right? Keep your two prompts, your predictions, and the actual top candidates for the lab questions.

---

## Part 3: Lab Questions (5 minutes)

Create a plain text file called `lab1_results.txt` and start it with:

```text
Names: Your name and your lab partner's name
Lab: Week 1 (The Prediction Machine)
Date: Today's date
```

Now answer **(without using GenAI)**:

1. **Warm-up (Task 0) and your review (Task 1):** How did the answer to "What does generative mean?" change across your three runs? What was your hard-to-label review, and did the model label it correctly?
2. **Peaked vs. spread (Task 2):** What were your two prompts? What did you predict, what were the actual top candidates, and were you right?

*There's no right or wrong answer here, I just want to see some thought go into the response. Base your answers on what you actually saw in this lab, and feel free to ask me any questions.*

---

## Submission

Upload (or copy-paste) `lab1_results.txt` to the **Week 1 Lab** assignment on D2L/Brightspace. If you worked with a partner, both partners should upload a copy.

Congrats, you're done with the first lab! Yippee! 🎉

---

## Optional (if you finish early, or at home)

- **Bigger isn't always better (the chapter's Warm-Up 2).** Ask a smaller model, such as `llama3.2:1b`, and `gemma4` the chapter's setup question (pass `model="llama3.2:1b"` to `ask`). What do you gain and lose as the model shrinks?
- **Find your own long shot.** Pick a prompt from Task 2 and find a candidate the model gave less than 1%. Pass it as `reply_start=` and plot the next step, the way "New" led to "York." Does the model build confidently on a word it barely believed in?
- **Paying attention (the chapter's Exercise 2).** To predict the next word, a model first has to decide which earlier words matter most. That's *attention*, and the chapter watches it by reading the attention heads of BERT, a small language model. First download BERT (about 420 MB, one time only):
  ```bash
  uv run python -c "from transformers import BertModel, BertTokenizer; BertTokenizer.from_pretrained('bert-base-uncased'); BertModel.from_pretrained('bert-base-uncased')"
  ```
  Then create `labs/week01/attention.py`:
  ```python
  from genai.viz import plot_attention, plot_attention_votes

  # One word changes, and "it" points somewhere else
  plot_attention([
      "The cat sat on the laptop because it was tired.",
      "The cat sat on the laptop because it was warm.",
  ], pronoun="it", path="labs/week01/attention_it.png")

  # All 144 of BERT's heads vote on what "standing" attends to most
  plot_attention_votes("She opened the door and saw a man standing.",
                       word="standing",
                       path="labs/week01/attention_standing.png")
  ```
  A tired "it" should lean on the cat; a warm "it" should lean on the laptop. Now write two sentences of your own that differ by one word, where that word changes which noun a pronoun points back to ("The trophy didn't fit in the suitcase because it was too *big*" versus "…too *small*"). Predict the answer first, then swap them in (setting `pronoun=` to your pronoun). Does the single head lean where you expected, and does the 144-head vote agree?
