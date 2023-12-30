class ClassSession:
  def __init__(
      self,
      sessionStartTime, 
      className,
      instructor,
      time,
      dayOfTheWeek,
      season,
      date,
      classType,
      level):
    self.sessionStartTime = sessionStartTime
    self.className = className
    self.instructor = instructor
    self.time = time
    self.dayOfTheWeek = dayOfTheWeek
    self.season = season
    self.date = date
    self.classType = classType
    self.level = level