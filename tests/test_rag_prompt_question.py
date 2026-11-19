import io
import json
import unittest
from contextlib import chdir, redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import rag_prompt_question


class RagPromptQuestionTest(unittest.TestCase):
    def test_writes_generated_messages_to_question_file(self):
        question = "¿Cómo se reprograma una entrega?"
        messages = [
            {"role": "system", "content": "Respondé con el contexto."},
            {"role": "user", "content": f"Contexto de la política\n{question}"},
        ]
        stdout = io.StringIO()

        for existing_content in (None, "Contenido anterior\n" * 100):
            with (
                self.subTest(file_exists=existing_content is not None),
                TemporaryDirectory() as directory,
                chdir(directory),
                patch("sys.argv", ["rag_prompt_question.py"]),
                patch("sys.stdin", io.StringIO(f"  {question}  \n")),
                patch("rag_prompt_question.generate_answer", return_value=messages) as generate,
                redirect_stdout(stdout),
            ):
                output = Path("question.md")
                if existing_content is not None:
                    output.write_text(existing_content, encoding="utf-8")

                self.assertEqual(rag_prompt_question.main(), 0)
                generate.assert_called_once_with(question)
                self.assertEqual(json.loads(output.read_text(encoding="utf-8")), messages)

        self.assertEqual(stdout.getvalue(), "")

    def test_reads_question_argument_without_waiting_for_stdin(self):
        question = "¿Qué hago si el destinatario no está en casa?"

        with (
            TemporaryDirectory() as directory,
            chdir(directory),
            patch("sys.argv", ["rag_prompt_question.py", question]),
            patch("sys.stdin") as stdin,
            patch("rag_prompt_question.generate_answer", return_value=[]) as generate,
        ):
            self.assertEqual(rag_prompt_question.main(), 0)
            stdin.readline.assert_not_called()
            generate.assert_called_once_with(question)
            self.assertTrue(Path("question.md").is_file())

    def test_rejects_blank_input_without_overwriting_file(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            TemporaryDirectory() as directory,
            chdir(directory),
            patch("sys.argv", ["rag_prompt_question.py"]),
            patch("sys.stdin", io.StringIO("  \n")),
            patch("rag_prompt_question.generate_answer") as generate,
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            output = Path("question.md")
            output.write_text("Contenido anterior", encoding="utf-8")
            self.assertNotEqual(rag_prompt_question.main(), 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "Contenido anterior")

        generate.assert_not_called()
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("pregunta", stderr.getvalue())
