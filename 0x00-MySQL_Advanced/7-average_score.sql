-- Create the ComputeAverageScoreForUser stored procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_average_score FLOAT;

    -- Compute the average score for the given user
    SELECT AVG(score) INTO v_average_score
    FROM corrections
    WHERE user_id = p_user_id;

    -- Update the average_score for the user
    UPDATE users
    SET average_score = v_average_score
    WHERE id = p_user_id;
END //
DELIMITER ;
