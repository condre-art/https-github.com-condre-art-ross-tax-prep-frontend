from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ORM Models ---
class EmployeeORM(Base):
	__tablename__ = "employees"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	email = Column(String, nullable=False)
	tenant_id = Column(String, nullable=False)
	status = Column(String, default="active")
	hire_date = Column(DateTime, nullable=True)

class PaystubORM(Base):
	__tablename__ = "paystubs"
	id = Column(Integer, primary_key=True, index=True)
	employee_id = Column(Integer, nullable=False)
	period_start = Column(DateTime, nullable=False)
	period_end = Column(DateTime, nullable=False)
	gross_pay = Column(Integer, nullable=False)
	net_pay = Column(Integer, nullable=False)
	taxes_withheld = Column(Integer, nullable=False)
	tenant_id = Column(String, nullable=False)

class TimecardORM(Base):
	__tablename__ = "timecards"
	id = Column(Integer, primary_key=True, index=True)
	employee_id = Column(Integer, nullable=False)
	date = Column(DateTime, nullable=False)
	hours_worked = Column(Integer, nullable=False)
	approved = Column(Integer, default=0)
	tenant_id = Column(String, nullable=False)

class PayrollORM(Base):
	__tablename__ = "payrolls"
	id = Column(Integer, primary_key=True, index=True)
	run_date = Column(DateTime, nullable=False)
	total_gross = Column(Integer, nullable=False)
	total_net = Column(Integer, nullable=False)
	tenant_id = Column(String, nullable=False)

class OnboardingORM(Base):
	__tablename__ = "onboardings"
	id = Column(Integer, primary_key=True, index=True)
	employee_id = Column(Integer, nullable=False)
	start_date = Column(DateTime, nullable=False)
	completed = Column(Integer, default=0)
	tenant_id = Column(String, nullable=False)

class HRCaseORM(Base):
	__tablename__ = "hrcases"
	id = Column(Integer, primary_key=True, index=True)
	employee_id = Column(Integer, nullable=False)
	opened = Column(DateTime, nullable=False)
	closed = Column(DateTime, nullable=True)
	case_type = Column(String, nullable=False)
	description = Column(String, nullable=False)
	status = Column(String, default="open")
	tenant_id = Column(String, nullable=False)
