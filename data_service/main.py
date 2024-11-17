import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


BASEDIR = Path(__file__).parent.parent
TECHNOLOGIES = [
    "django",
    "flask",
    "fastapi",
    "pyramid",
    "tornado",
    "bottle",
    "jinja2",
    "mako",
    "django templates",
    "pelican",
    "mkdocs",
    "webpack",
    "vite",
    "react",
    "vue.js",
    "angular",
    "django rest framework",
    "drf",
    "fastapi",
    "flask-restful",
    "graphene",
    "swagger",
    "openapi",
    "postman",
    "drf spectacular",
    "marshmallow",
    "pydantic",
    "postgresql",
    "mysql",
    "sqlite",
    "mariadb",
    "mongodb",
    "redis",
    "cassandra",
    "couchdb",
    "sqlalchemy",
    "django orm",
    "tortoise-orm",
    "peewee",
    "pony orm",
    "pandas",
    "numpy",
    "dask",
    "modin",
    "matplotlib",
    "seaborn",
    "plotly",
    "bokeh",
    "altair",
    "dash",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "xgboost",
    "lightgbm",
    "catboost",
    "nltk",
    "spacy",
    "transformers",
    "textblob",
    "pyarrow",
    "pyspark",
    "hadoop",
    "dask",
    "pydoop",
    "beautifulsoup",
    "scrapy",
    "selenium",
    "requests",
    "lxml",
    "pyppeteer",
    "chromedriver",
    "puppeteer",
    "playwright",
    "aws",
    "boto3",
    "azure sdk",
    "google cloud platform",
    "gcp sdk",
    "docker",
    "docker compose",
    "podman",
    "kubernetes",
    "helm",
    "github actions",
    "gitlab ci/cd",
    "jenkins",
    "circleci",
    "travis ci",
    "terraform",
    "ansible",
    "pulumi",
    "pytest",
    "unittest",
    "nose",
    "behave",
    "unittest.mock",
    "pytest-mock",
    "pylint",
    "flake8",
    "mypy",
    "black",
    "pyautogui",
    "fabric",
    "invoke",
    "selenium",
    "autoit",
    "celery",
    "apscheduler",
    "airflow",
    "requests",
    "httpx",
    "socket",
    "paramiko",
    "pycryptodome",
    "hashlib",
    "pyjwt",
    "cryptography",
    "pygame",
    "panda3d",
    "godot",
    "pyglet",
    "arcade",
    "tkinter",
    "pyqt",
    "kivy",
    "wxpython",
    "pygtk",
    "micropython",
    "circuitpython",
    "raspberry pi",
    "gpio zero",
    "picamera",
    "aws iot sdk",
    "azure iot sdk",
    "openai gym",
    "stable-baselines",
    "mlflow",
    "ros",
    "pyrobot",
    "pybullet",
    "openpyxl",
    "xlrd",
    "xlwt",
    "pypdf2",
    "reportlab",
    "pdfplumber",
    "pil",
    "pillow",
    "opencv",
    "imageai",
    "pydub",
    "librosa",
    "wave",
    "web3.py",
    "bitcoinlib",
    "brownie",
    "vyper",
    "scipy",
    "sympy",
    "simpy",
    "venv",
    "virtualenv",
    "conda",
    "pip",
    "poetry",
    "pipenv",
    "pycharm",
    "visual studio code",
    "jupyter notebook",
    "spyder",
    "black",
    "isort",
    "mypy",
    "flake8",
    "pdb",
    "ipdb",
    "socket.io",
    "websocket api",
    "celery",
    "rq",
    "smtplib",
    "flask-mail",
    "django-email",
    "loguru",
    "sentry",
    "prometheus",
    "dynaconf",
    "dotenv",
    "configparser",
]


class DataAnalyzer:
    EXP_RANGE = {
        "junior": "0-1",
        "strong_junior": "1-3",
        "middle": "3-5",
        "senior": "5+",
    }

    def __init__(self, csv_path, tech_list):
        self.df = pd.read_csv(csv_path)
        self.tech_list = tech_list
        self.expanded_df = None
        self.tech_counts = None

    def find_technologies(self, description):
        description_words = set(description.split(","))
        intersection = description_words.intersection(set(self.tech_list))
        return list(intersection)

    def add_years_to_experience(self):
        self.df["years_range"] = self.df["experience"].apply(lambda x: self.EXP_RANGE.get(x, "Unknown"))

    def process_data(self):
        self.df["technologies"] = self.df["description"].apply(lambda x: self.find_technologies(x))
        self.add_years_to_experience()
        self.expanded_df = self.df.explode("technologies").dropna(subset=["technologies"])

    def count_technologies_by_experience(self):
        self.tech_counts = self.expanded_df.groupby(['experience', 'technologies']).size().reset_index(name='count')

    def plot_charts(self):
        experience_levels = self.tech_counts['experience'].unique()

        max_count = self.tech_counts['count'].max()

        fig, axes = plt.subplots(nrows=len(experience_levels), ncols=1, figsize=(16, 5 * len(experience_levels)),
                                 sharex=False)

        for i, exp in enumerate(experience_levels):
            exp_data = self.tech_counts[self.tech_counts['experience'] == exp]
            exp_data = exp_data.sort_values(by='count', ascending=False)

            axes[i].bar(exp_data['technologies'], exp_data['count'], color='steelblue')
            axes[i].set_title(f"{exp.capitalize()} Level ({self.EXP_RANGE.get(exp, 'Unknown')} years)")
            axes[i].set_ylabel('Count')
            axes[i].set_xlabel('Technologies')
            axes[i].set_xticks(range(len(exp_data['technologies'])))
            axes[i].set_xticklabels(exp_data['technologies'], rotation=45, ha='right')

            axes[i].set_ylim(0, max_count)

        fig.supxlabel('Technologies')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    BASEDIR = Path(__file__).parent.parent
    csv_path = BASEDIR / "data" / "vacancy_list.csv"

    analyzer = DataAnalyzer(csv_path, TECHNOLOGIES)
    analyzer.process_data()
    analyzer.count_technologies_by_experience()
    analyzer.plot_charts()
