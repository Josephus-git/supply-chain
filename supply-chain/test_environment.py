# This will test the environment to ensure that the .env file is set up
# correctly and that the Ollama (Llama 3.2) and Neo4j connections are working.
import os
import unittest

from dotenv import load_dotenv, find_dotenv
load_dotenv()

class TestEnvironment(unittest.TestCase):

    skip_env_variable_tests = True
    skip_ollama_test = True
    skip_neo4j_test = True

    def test_env_file_exists(self):
        env_file_exists = True if find_dotenv() > "" else False
        if env_file_exists:
            TestEnvironment.skip_env_variable_tests = False
        self.assertTrue(env_file_exists, ".env file not found.")

    def env_variable_exists(self, variable_name):
        self.assertIsNotNone(
            os.getenv(variable_name),
            f"{variable_name} not found in .env file"
        )

    def test_ollama_variables(self):
        if TestEnvironment.skip_env_variable_tests:
            self.skipTest("Skipping Ollama env variable test")

        self.env_variable_exists('OLLAMA_MODEL')
        TestEnvironment.skip_ollama_test = False

    def test_neo4j_variables(self):
        if TestEnvironment.skip_env_variable_tests:
            self.skipTest("Skipping Neo4j env variables test")

        self.env_variable_exists('NEO4J_URI')
        self.env_variable_exists('NEO4J_USERNAME')
        self.env_variable_exists('NEO4J_PASSWORD')
        self.env_variable_exists('NEO4J_DATABASE')
        TestEnvironment.skip_neo4j_test = False

    def test_ollama_connection(self):
        if TestEnvironment.skip_ollama_test:
            self.skipTest("Skipping Ollama test")

        from langchain_ollama import ChatOllama

        model_name = os.getenv('OLLAMA_MODEL', 'llama3.2')
        llm = ChatOllama(model=model_name)

        try:
            response = llm.invoke("ping")
        except Exception:
            response = None

        self.assertIsNotNone(
            response,
            f"Ollama connection failed for model '{model_name}'. Ensure Ollama server is running locally."
        )

    def test_neo4j_connection(self):
        msg = "Neo4j connection failed. Check the NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE values in .env file."
        connected = False

        if TestEnvironment.skip_neo4j_test:
            self.skipTest("Skipping Neo4j connection test")

        from neo4j import GraphDatabase

        driver = GraphDatabase.driver(
            os.getenv('NEO4J_URI'),
            auth=(os.getenv('NEO4J_USERNAME'), 
                  os.getenv('NEO4J_PASSWORD'))
        )
        try:
            driver.verify_connectivity()
            try:
                driver.execute_query("RETURN true", database_=os.getenv('NEO4J_DATABASE'))
                connected = True
            except Exception:
                msg = "Neo4j database query failed. Check the NEO4J_DATABASE value in .env file."
        except Exception:
            msg = "Neo4j verify connection failed. Check the NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD values in .env file."
        finally:
            driver.close()

        self.assertTrue(connected, msg)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEnvironment('test_env_file_exists'))
    suite.addTest(TestEnvironment('test_ollama_variables'))
    suite.addTest(TestEnvironment('test_neo4j_variables'))
    suite.addTest(TestEnvironment('test_ollama_connection'))
    suite.addTest(TestEnvironment('test_neo4j_connection'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())