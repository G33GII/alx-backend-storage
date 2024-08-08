-- Create the ComputeAverageWeightedScoreForUser stored procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_total_weighted_score FLOAT;
    DECLARE v_total_weight INT;
    DECLARE v_average_weighted_score FLOAT;

    -- Calculate total weighted score and total weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO v_total_weighted_score, v_total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = p_user_id;

    -- Compute the average weighted score
    IF v_total_weight > 0 THEN
        SET v_average_weighted_score = v_total_weighted_score / v_total_weight;
    ELSE
        SET v_average_weighted_score = 0;
    END IF;

    -- Update the average_score for the user
    UPDATE users
    SET average_score = v_average_weighted_score
    WHERE id = p_user_id;
END //
DELIMITER ;
