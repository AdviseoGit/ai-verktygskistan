import sys
import os
sys.path.append(os.getcwd())

with open("/data/workspace/projects/ai-verktygskistan/models.py", "r") as f:
    content = f.read()

new_content = content + """
class CalcData(Base):
    __tablename__ = "calc_data"

    id = Column(Integer, primary_key=True, index=True)
    employees = Column(Integer)
    salary = Column(Integer)
    industry = Column(String)
    saved_value = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
"""
with open("/data/workspace/projects/ai-verktygskistan/models.py", "w") as f:
    f.write(new_content)

