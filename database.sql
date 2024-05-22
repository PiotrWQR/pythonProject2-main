CREATE TABLE IF NOT EXISTS `Skladnik` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT ,
  `Nazwa` VARCHAR(45) NULL,
  `Kalorie_Na_Jednostke` INT UNSIGNED NULL,
  `Dodatkowe` VARCHAR(45) NULL
  );


CREATE TABLE IF NOT EXISTS `posrednia_skladnik_jednostka` (
  `Skladnik_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Ilosc` INT NOT NULL,
  `Jednostka_Jednostka` VARCHAR(10) NOT NULL,
  -- INDEX `fk_posrednia_skladnik_jednostka_Skladnik1_idx` (`Skladnik_ID` ASC),
  CONSTRAINT `fk_posrednia_skladnik_jednostka_Skladnik1`
    FOREIGN KEY (`Skladnik_ID`)
    REFERENCES `Skladnik` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posrednia_skladnik_jednostka_Jednostka1`
    FOREIGN KEY (`Jednostka_Jednostka`)
    REFERENCES `Jednostka` (`Jednostka`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



CREATE TABLE IF NOT EXISTS `Jednostka` (
  `Jednostka` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`Jednostka`));

CREATE TABLE IF NOT EXISTS `Posiłek` (
  `ID` INT NOT NULL,
  `Administrator_nazwa_identyfikacyjna` VARCHAR(30) NOT NULL,
  `Nazwa` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`, `Administrator_nazwa_identyfikacyjna`),
  INDEX `fk_Posiłek_Administrator1_idx` (`Administrator_nazwa_identyfikacyjna` ASC),
  CONSTRAINT `fk_Posiłek_Administrator1`
    FOREIGN KEY (`Administrator_nazwa_identyfikacyjna`)
    REFERENCES `sakila`.`Administrator` (`nazwa_identyfikacyjna`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)





INSERT INTO Jednostka values ('sztuk');
INSERT INTO Jednostka values ('łyżeczek');
INSERT INTO Jednostka values ('szklanek');
INSERT INTO Jednostka values ('łyżek');
INSERT INTO Jednostka values ('mililitrów');
INSERT INTO Jednostka values ('litrów');










 insert into Administrator values('Admin','alfa@alfa.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');+