from .article import Article
from .stance import PoliticalStance, Classification, Consensus
from .database import Base, ArticleModel, ClassificationModel, ConsensusModel

__all__ = [
    "Article", "PoliticalStance", "Classification", "Consensus",
    "Base", "ArticleModel", "ClassificationModel", "ConsensusModel"
]

"""
__init__.py Files:
These files make a directory a Python package
They can be empty or contain initialization code
They control what gets imported when someone does from package import *

This file is used to expose the Article model/class to the outside world
When someone does from app.models import * 

(__all__ Acts as a public interface for the package, Prevents private/internal names from being exposed)
They will get this file's __all__ list
"""