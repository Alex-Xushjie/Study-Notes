from sqlalchemy import Column, Date, DateTime, DECIMAL, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(50), nullable=False)
    department = Column(String(100), nullable=True)
    role = Column(String(20), nullable=False, default="employee")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    timesheets = relationship("TimesheetEntry", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(100), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    tickets = relationship("Ticket", back_populates="project")
    timesheets = relationship("TimesheetEntry", back_populates="project")


class WorkType(Base):
    __tablename__ = "work_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    timesheets = relationship("TimesheetEntry", back_populates="work_type")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_no = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    ticket_type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="open")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="tickets")
    timesheets = relationship("TimesheetEntry", back_populates="ticket")


class TimesheetEntry(Base):
    __tablename__ = "timesheet_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    work_date = Column(Date, nullable=False)
    work_type_id = Column(Integer, ForeignKey("work_types.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    hours = Column(DECIMAL(4, 2), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="timesheets")
    project = relationship("Project", back_populates="timesheets")
    work_type = relationship("WorkType", back_populates="timesheets")
    ticket = relationship("Ticket", back_populates="timesheets")