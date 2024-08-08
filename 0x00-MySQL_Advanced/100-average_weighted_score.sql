DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_score_sum FLOAT DEFAULT 0;
    DECLARE average_weighted_score FLOAT DEFAULT 0;

    -- Calculate the sum of the weighted scores and total weight for the given user
    SELECT SUM(p.weight * c.score), SUM(p.weight)
    INTO weighted_score_sum, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Compute the average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = weighted_score_sum / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    -- Update the user's average_score
    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = user_id;
END $$

DELIMITER ;
